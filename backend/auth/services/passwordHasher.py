"""Password hashing for the users table.

Passwords are stored as a salted PBKDF2-HMAC-SHA256 hash. Each user has a
random per-user salt (stored in its own ``salt`` column) so that two users with
the same password get different stored hashes and precomputed ("rainbow table")
attacks are useless.

The iteration count is a hardcoded constant rather than stored per-row: every
hash in this app uses the same work factor, so there is nothing per-row to
record. (The tradeoff: raising ITERATIONS later invalidates existing hashes and
would require a password reset — acceptable for this project.)
"""

import hashlib
import hmac
import os

ITERATIONS = 200_000
SALT_BYTES = 16


def _pbkdf2(plain: str, salt: bytes) -> str:
    """Return the PBKDF2-HMAC-SHA256 hash of ``plain`` with ``salt`` as hex."""
    digest = hashlib.pbkdf2_hmac("sha256", plain.encode("utf-8"), salt, ITERATIONS)
    return digest.hex()


def hash_password(plain: str) -> tuple[str, str]:
    """Hash ``plain`` with a fresh random salt.

    Returns ``(hash_hex, salt_hex)`` — the caller stores each in its own column.
    """
    salt = os.urandom(SALT_BYTES)
    return _pbkdf2(plain, salt), salt.hex()


def verify_password(plain: str, stored_hash: str, salt_hex: str) -> bool:
    """Return True if ``plain`` matches ``stored_hash`` under ``salt_hex``."""
    try:
        salt = bytes.fromhex(salt_hex)
    except (ValueError, TypeError):
        return False
    candidate = _pbkdf2(plain, salt)
    # constant-time comparison to avoid leaking match progress via timing
    return hmac.compare_digest(candidate, stored_hash)
