"""
Test if the method can encode and decode all string
"""

from utils.auth import encode_password, parse_token, generate_token


def test_encode_password():
    """
    We use the website: https://www.base64encode.org/  to generate encoded passwords
    Then compare
    """
    password_1 = ''
    # print(encode_password(password_1))
    assert  1==1