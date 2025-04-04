from rest_framework.exceptions import APIException

class PasswordNotMatch(APIException):
    status_code = 400
    default_detail = 'Passwords not match.'
    default_code = 'password not match'

class EmailExistAlready(APIException):
    status_code = 400
    default_detail = 'An account with this email already exists.'
    default_code = 'email exist'

class EmailOrPasswordIncorrect(APIException):
    status_code = 400
    default_detail = 'Invalid email or password.'
    default_code = 'email or password incorrect'

class NotVerified(APIException):
    status_code = 400
    default_detail = 'Please verify your account before logging in.'
    default_code = 'not verified'

class UserAlreadyVerified(APIException):
    status_code = 409
    default_detail = 'This account has already been verified.'
    default_code = 'already verified'

class IncorrectUrl(APIException):
    status_code = 400
    default_detail = 'Invalid link.'
    default_code = 'incorrect link'

class IncorrectToken(APIException):
    status_code = 400
    default_detail = 'Token invalid or expired'
    default_code = 'incorrect token'
