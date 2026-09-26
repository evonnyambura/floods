import re


def sanitize_text_field(
    value: str,
    field_name: str
) -> str:
    value = value.strip()

    if not value:
        raise ValueError(
            f"{field_name} cannot be empty."
        )

    if len(value) > 100:
        raise ValueError(
            f"{field_name} is too long."
        )

    if not re.fullmatch(
        r"[A-Za-zÀ-ÖØ-öø-ÿ\s'-]+",
        value
    ):
        raise ValueError(
            f"{field_name} contains invalid characters."
        )

    return value


def validate_strong_password(
    password: str
) -> str:

    if len(password) < 8:
        raise ValueError(
            "Password must be at least 8 characters long."
        )

    if not re.search(r"[A-Z]", password):
        raise ValueError(
            "Password must contain at least one uppercase letter."
        )

    if not re.search(r"[a-z]", password):
        raise ValueError(
            "Password must contain at least one lowercase letter."
        )

    if not re.search(r"\d", password):
        raise ValueError(
            "Password must contain at least one number."
        )

    if not re.search(r"[^\w\s]", password):
        raise ValueError(
            "Password must contain at least one special character."
        )

    return password