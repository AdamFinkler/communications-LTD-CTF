import re

from auth.services.passwordHasher import hash_password, verify_password


def test_hash_password_returns_hash_and_salt():
    hash_hex, salt_hex = hash_password("Secure@99")
    # both are non-empty hex strings
    assert hash_hex and re.fullmatch(r"[0-9a-f]+", hash_hex)
    assert salt_hex and re.fullmatch(r"[0-9a-f]+", salt_hex)


def test_hash_is_not_the_plaintext():
    hash_hex, _ = hash_password("Secure@99")
    assert "Secure@99" not in hash_hex


def test_verify_accepts_correct_password():
    hash_hex, salt_hex = hash_password("Secure@99")
    assert verify_password("Secure@99", hash_hex, salt_hex) is True


def test_verify_rejects_wrong_password():
    hash_hex, salt_hex = hash_password("Secure@99")
    assert verify_password("wrong-password", hash_hex, salt_hex) is False


def test_same_password_produces_different_salt_and_hash():
    # random per-password salt means two hashes of the same password differ
    hash_a, salt_a = hash_password("Secure@99")
    hash_b, salt_b = hash_password("Secure@99")
    assert salt_a != salt_b
    assert hash_a != hash_b
    # ...yet both still verify
    assert verify_password("Secure@99", hash_a, salt_a)
    assert verify_password("Secure@99", hash_b, salt_b)


def test_verify_rejects_when_salt_does_not_match():
    hash_hex, _ = hash_password("Secure@99")
    _, other_salt = hash_password("Secure@99")
    # correct password + hash, but the wrong salt must not verify
    assert verify_password("Secure@99", hash_hex, other_salt) is False


def test_verify_rejects_tampered_hash():
    hash_hex, salt_hex = hash_password("Secure@99")
    # flip the last hex char
    tampered = hash_hex[:-1] + ("0" if hash_hex[-1] != "0" else "1")
    assert verify_password("Secure@99", tampered, salt_hex) is False
