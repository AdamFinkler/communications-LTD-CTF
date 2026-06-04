import html


def encode_input(value: str) -> str:
    """HTML-entity-encode a user-supplied string (XSS hardening on write)."""
    return html.escape(value, quote=True)
