from rest_framework.exceptions import APIException

class NoObjectWithThisSug(APIException):
    status_code = 404
    default_detail = 'No object with this slug.'
    default_code = 'not found'