from auth.services.inputSanitizer import encode_input


def test_encodes_each_dangerous_char():
    assert encode_input("&") == "&amp;"
    assert encode_input("<") == "&lt;"
    assert encode_input(">") == "&gt;"
    assert encode_input('"') == "&quot;"
    assert encode_input("'") == "&#x27;"


def test_clean_name_passes_through_unchanged():
    assert encode_input("Alice Cohen") == "Alice Cohen"


def test_empty_string_returns_empty_string():
    assert encode_input("") == ""


def test_script_payload_becomes_inert():
    assert encode_input("<script>alert(1)</script>") == (
        "&lt;script&gt;alert(1)&lt;/script&gt;"
    )
