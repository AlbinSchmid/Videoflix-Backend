from rest_framework.exceptions import APIException

class NoObjectWithThisSug(APIException):
    """Exception raised when no object with the given slug is found."""
    status_code = 404
    default_detail = 'No object with this slug.'
    default_code = 'not found'