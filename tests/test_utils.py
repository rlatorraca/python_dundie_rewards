import pytest

from dundie.utils.email import check_valid_email
from dundie.utils.user import generate_random_simple_password


@pytest.mark.unit
@pytest.mark.high
@pytest.mark.parametrize("email_address", ["rlsp@gmail.com", "joe@doe.com.br", "maria@terra.com.ca"])
def test_positive_check_valid_email(email_address):
    """Ensure email address is valid"""
    assert check_valid_email(email_address) is True


@pytest.mark.unit
@pytest.mark.high
@pytest.mark.parametrize("email_address", ["rlsp@.com", "@doe.com.br", "maria@terra"])
def test_negative_check_valid_email(email_address):
    """Check if email address is valid"""
    assert check_valid_email(email_address) is False
    assert check_valid_email(email_address) is False


@pytest.mark.unit
@pytest.mark.high
def test_positive_generate_simple_password():
    """Test generate random unique simple password

    TODO: Generate Hashed complex passwords, and encrypt those"
    """
    passwords = []
    for _ in range(100):
        passwords.append(generate_random_simple_password(12))
    print(passwords)
    assert len(set(passwords)) == 100
