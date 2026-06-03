import hashlib
import hmac
import json
import os
import re
import secrets
from pathlib import Path

CONFIG_PATH = Path(__file__).resolve().parents[3] / "password_configuration.json"

_login_attempts: dict[str, int] = {}
_reset_tokens: dict[str, str] = {}
_verified_reset_emails: set[str] = set()


def load_password_config() -> dict:
    with open(CONFIG_PATH, encoding="utf-8") as config_file:
        return json.load(config_file)


def generate_salt() -> str:
    return secrets.token_hex(16)


def hash_password(password: str, salt: str) -> str:
    return hmac.new(
        salt.encode("utf-8"),
        password.encode("utf-8"),
        hashlib.sha256,
    ).hexdigest()


def verify_password(password: str, salt: str, stored_hash: str) -> bool:
    return hmac.compare_digest(hash_password(password, salt), stored_hash)


def validate_password(password: str, username: str = "") -> tuple[bool, str]:
    config = load_password_config()
    min_length = int(config.get("min_length", 10))

    if len(password) < min_length:
        return False, f"Password must be at least {min_length} characters"

    if config.get("must_contain_upper", "true") == "true" and not re.search(r"[A-Z]", password):
        return False, "Password must contain an uppercase letter"

    if config.get("must_contain_lower", "true") == "true" and not re.search(r"[a-z]", password):
        return False, "Password must contain a lowercase letter"

    if config.get("must_contain_digit", "true") == "true" and not re.search(r"\d", password):
        return False, "Password must contain a digit"

    if config.get("must_contain_special", "true") == "true" and not re.search(
        r"[!@#$%^&*(),.?\":{}|<>]", password
    ):
        return False, "Password must contain a special character"

    known_passwords = config.get("known_passwords", [])
    if isinstance(known_passwords, str):
        known_passwords = [known_passwords]

    lowered = password.lower()
    for blocked in known_passwords:
        if blocked and blocked.lower() in lowered:
            return False, "Password is too common or appears in the blocked dictionary"

    if username and username.lower() in lowered:
        return False, "Password must not contain the username"

    return True, ""


def check_password_history(username: str, new_password: str, salt: str) -> tuple[bool, str]:
    from database.connection import cursor

    config = load_password_config()
    history_limit = int(config.get("password_history_counter", 3))
    new_hash = hash_password(new_password, salt)

    cursor.execute(
        f"""
        SELECT password_hash FROM password_history
        WHERE username = '{username}'
        ORDER BY id DESC
        LIMIT {history_limit}
        """
    )

    for row in cursor.fetchall():
        if row[0] == new_hash:
            return False, f"Password was used recently. Choose a password not in the last {history_limit} passwords"

    return True, ""


def save_password_history(username: str, password_hash: str) -> None:
    from database.connection import connection, cursor

    cursor.execute(
        f"""
        INSERT INTO password_history (username, password_hash)
        VALUES ('{username}', '{password_hash}')
        """
    )
    connection.commit()


def record_login_failure(username: str) -> tuple[bool, str]:
    config = load_password_config()
    max_attempts = int(config.get("max_login_attempts", 3))
    _login_attempts[username] = _login_attempts.get(username, 0) + 1

    if _login_attempts[username] >= max_attempts:
        return False, f"Account locked after {max_attempts} failed login attempts"

    remaining = max_attempts - _login_attempts[username]
    return False, f"Wrong username or password. {remaining} attempt(s) remaining"


def clear_login_attempts(username: str) -> None:
    _login_attempts.pop(username, None)


def is_login_locked(username: str) -> tuple[bool, str]:
    config = load_password_config()
    max_attempts = int(config.get("max_login_attempts", 3))

    if _login_attempts.get(username, 0) >= max_attempts:
        return True, f"Account locked after {max_attempts} failed login attempts"

    return False, ""


def create_reset_token(email: str) -> str:
    random_value = secrets.token_hex(16)
    token = hashlib.sha1(random_value.encode("utf-8")).hexdigest()
    _reset_tokens[email] = token
    return token


def verify_reset_token(email: str, code: str) -> bool:
    stored = _reset_tokens.get(email)
    if stored and hmac.compare_digest(stored, code.strip()):
        _verified_reset_emails.add(email)
        _reset_tokens.pop(email, None)
        return True
    return False


def is_reset_verified(email: str) -> bool:
    return email in _verified_reset_emails


def clear_reset_verification(email: str) -> None:
    _verified_reset_emails.discard(email)
