import json
from pathlib import Path
from auth.services.passwordHasher import verify_password


_CONFIG_PATH = Path(__file__).parent.parent.parent.parent / "password_configuration.json"
_SPECIAL_CHARS = set("!@#$%^&*()_+-=[]{}|;':\",./<>?")


def _load_config() -> dict:
    with _CONFIG_PATH.open("r", encoding="utf-8") as f:
        return json.load(f)


try:
    _CONFIG = _load_config()
except (FileNotFoundError, json.JSONDecodeError) as e:
    raise RuntimeError(f"Could not load password_configuration.json: {e}") from e


def _is_enabled(value) -> bool:
    if isinstance(value, bool):
        return value
    return str(value).lower() == "true"


def validate_password(password: str, config: dict| None = None) -> list[str]:
    """Return a list of rule-violation messages. Empty list means the password is valid."""
    if config is None:
        config = _CONFIG

    errors = []

    min_length = int(config.get("min_length", 8))
    if len(password) < min_length:
        errors.append(f"Password must be at least {min_length} characters long.")

    if _is_enabled(config.get("must_contain_upper", False)):
        if not any(c.isupper() for c in password):
            errors.append("Password must contain at least one uppercase letter.")

    if _is_enabled(config.get("must_contain_lower", False)):
        if not any(c.islower() for c in password):
            errors.append("Password must contain at least one lowercase letter.")

    if _is_enabled(config.get("must_contain_digit", False)):
        if not any(c.isdigit() for c in password):
            errors.append("Password must contain at least one digit.")

    if _is_enabled(config.get("must_contain_special", False)):
        if not any(c in _SPECIAL_CHARS for c in password):
            errors.append("Password must contain at least one special character (!@#$%^&* etc.).")

    known_raw = config.get("known_passwords", "")
    known = {p.strip() for p in known_raw.split(",") if p.strip()}
    if password.lower() in {p.lower() for p in known}:
        errors.append("Password is too common, please choose a stronger one.")

    return errors
