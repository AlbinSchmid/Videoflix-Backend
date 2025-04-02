from rest_framework.exceptions import APIException

class PasswordNotMatch(APIException):
    status_code = 400
    default_detail = 'Passwords not match.'
    default_code = 'password not match'


class EmailExistAlready(APIException):
    status_code = 400
    default_detail = 'An account with this email already exists.'
    default_code = 'email exist'
