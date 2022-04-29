"""
Test if the method can encode and decode all string
"""

from utils.auth import encode_password, parse_token, generate_token


def test_encode_password():
    """
    We use the website: https://www.base64encode.org/  to generate encoded  base64 passwords
    Then pass base64 password to the weibsite: http://www.md5.cz/ to generate the md5 passwords(this is the one we want to validate)
    Then compare
    """

    # special cases
    pwd = ''
    assert encode_password(pwd) == ''

    pwd = None
    assert encode_password(pwd) == None

    # normal cases
    pwd = ' '
    assert encode_password(pwd) == '99adb8db68a29fad97854d98642d1a79'

    pwd = 'Ji20fmvfd-124@!450otk32;'
    print(encode_password(pwd))
    assert encode_password(pwd) == 'de68fb677948f7e14b6f62b88000a92b'

    pwd = '  .  sodwp0351 =2..........;'
    assert encode_password(pwd) == '5e7d9e351a0fd0050fe16d8335e8f391'


def test_token():
    """
    generate_token encode the payload and return a token
    parse_token decode the token and return a payload
    """
    # special case
    payload = {}
    assert parse_token(generate_token(payload)) == payload

    payload = None
    assert parse_token(generate_token(payload)) == payload

    # normal case
    payload = {'name': 'Tom Cat', 'age': 99, 'sex': 'male', 'active': True}
    assert parse_token(generate_token(payload)) == payload
    payload = {'name': '', 'age': 99, 'sex': 'male', 'active': False,'status':None,}
    assert parse_token(generate_token(payload)) == payload