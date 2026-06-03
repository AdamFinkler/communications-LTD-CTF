import pytest
from auth.services.passwordValidator import validate_password


# We pass a config dict directly so tests don't depend on the JSON file on disk.
BASE_CONFIG = {
    "min_length": "8",
    "must_contain_upper": "true",
    "must_contain_lower": "true",
    "must_contain_special": "true",
    "must_contain_digit": "true",
    "known_passwords": "12345678,password1",
}


def test_valid_password_returns_no_errors():
    errors = validate_password("Secure@99", BASE_CONFIG)
    assert errors == []


def test_too_short_returns_error():
    errors = validate_password("Ab1@", BASE_CONFIG)
    assert any("8" in e for e in errors)


def test_missing_uppercase_returns_error():
    errors = validate_password("secure@99", BASE_CONFIG)
    assert any("uppercase" in e.lower() for e in errors)


def test_missing_lowercase_returns_error():
    errors = validate_password("SECURE@99", BASE_CONFIG)
    assert any("lowercase" in e.lower() for e in errors)


def test_missing_digit_returns_error():
    errors = validate_password("Secure@!!", BASE_CONFIG)
    assert any("digit" in e.lower() for e in errors)


def test_missing_special_returns_error():
    errors = validate_password("Secure123", BASE_CONFIG)
    assert any("special" in e.lower() for e in errors)


def test_known_password_returns_error():
    errors = validate_password("12345678", BASE_CONFIG)
    assert any("common" in e.lower() for e in errors)


def test_multiple_failures_returns_multiple_errors():
    # all lowercase, no digit, no special — should return at least 3 errors
    errors = validate_password("abcdefgh", BASE_CONFIG)
    assert len(errors) >= 3


def test_disabled_rule_is_not_enforced():
    config = {**BASE_CONFIG, "must_contain_special": "false"}
    errors = validate_password("Secure123", config)
    assert errors == []


def test_empty_password_is_invalid():
    errors = validate_password("", BASE_CONFIG)
    assert len(errors) > 0
