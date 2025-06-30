class AppException(Exception): 
    def __init__(self, status_code: int, detail: str): 
        self.detail = detail
        self.status_code = status_code
        

class InvalidPasswordException(AppException): 
    pass

class AddressNotFoundException(AppException): 
    pass

class UserNotFoundException(AppException):
    pass

class UserEmailAlreadyExistsException(AppException):
    pass

class SamePasswordException(AppException): 
    pass

class InvalidTokenException(AppException): 
    pass

class UnauthorizedException(AppException): 
    pass
