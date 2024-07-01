import re  # Regular expression (REGEX)

regex = r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b"  # Regular expression


def check_valid_email(email_address):
    """Check if email address is valid"""
    return bool(re.fullmatch(regex, email_address))
