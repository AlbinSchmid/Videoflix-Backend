from rest_framework.exceptions import APIException

class PasswordNotMatch(APIException):
    """Exception raised when the password and confirm password do not match."""
    status_code = 400
    default_detail = 'Passwords not match.'
    default_code = 'password not match'

class EmailExistAlready(APIException):
    """Exception raised when the email already exists in the database."""
    status_code = 400
    default_detail = 'An account with this email already exists.'
    default_code = 'email exist'

class EmailOrPasswordIncorrect(APIException):
    """Exception raised when the email or password is incorrect."""
    status_code = 400
    default_detail = 'Invalid email or password.'
    default_code = 'email or password incorrect'

class NotVerified(APIException):
    """Exception raised when the user account is not verified."""
    status_code = 400
    default_detail = 'Please verify your account before logging in.'
    default_code = 'not verified'

class NotVerifiedForgotPassword(APIException):
    """Exception raised when the user account is not verified during password reset."""
    status_code = 400
    default_detail = 'Please verify your account before reset your password.'
    default_code = 'not verified'

class UserAlreadyVerified(APIException):
    """Exception raised when the user account is already verified."""
    status_code = 409
    default_detail = 'This account has already been verified.'
    default_code = 'already verified'

class IncorrectUrl(APIException):
    """Exception raised when the URL used for verification is incorrect."""
    status_code = 400
    default_detail = 'The link you used is invalid or no longer active.'
    default_code = 'incorrect link'

class UserNotFound(APIException):
    """Exception raised when the user is not found in the database."""
    status_code = 404
    default_detail = 'User with this email was not found.'
    default_code = 'user not found'

class PasswordSameAsOld(APIException):
    """Exception raised when the new password is the same as the old password."""
    status_code = 400
    default_detail = 'New password cannot be the same as the old one. Please choose a different password.'
    default_code = 'password same as old'

class UserNotExistWithThisEmail(APIException):
    """Exception raised when no user exists with the provided email."""
    status_code = 404
    default_detail = 'We couldn’t find an account with that email address.'
    default_code = 'user not found'

class IncorrectPassword(APIException):
    """Exception raised when the password provided is incorrect."""
    status_code = 400
    default_detail = 'The password you entered is incorrect.'
    default_code = 'incorrect password'

class UserNotLoggedIn(APIException):
    """Exception raised when the user is not logged in."""
    status_code = 401
    default_detail = 'Log in to your account to continue.'
    default_code = 'unauthorized'



