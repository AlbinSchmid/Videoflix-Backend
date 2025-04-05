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

class NotVerifiedForgotPassword(APIException):
    status_code = 400
    default_detail = 'Please verify your account before reset your password.'
    default_code = 'not verified'

class UserAlreadyVerified(APIException):
    status_code = 409
    default_detail = 'This account has already been verified.'
    default_code = 'already verified'

class IncorrectUrl(APIException):
    status_code = 400
    default_detail = 'The link you used is invalid or no longer active.'
    default_code = 'incorrect link'

class UserNotFound(APIException):
    status_code = 404
    default_detail = 'User with this email was not found.'
    default_code = 'user not found'

class PasswordSameAsOld(APIException):
    status_code = 400
    default_detail = 'New password cannot be the same as the old one. Please choose a different password.'
    default_code = 'password same as old'


