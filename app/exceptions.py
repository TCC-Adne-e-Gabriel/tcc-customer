from http import HTTPStatus

class AppException(Exception): 
    def __init__(self, status_code: int, detail: str): 
        self.detail = detail
        self.status_code = status_code
        super().__init__(detail)


class InvalidPasswordException(AppException): 
    def __init__(self):
        super().__init__(HTTPStatus.BAD_REQUEST, "Invalid password.")


class AddressNotFoundException(AppException): 
    def __init__(self):
        super().__init__(HTTPStatus.NOT_FOUND, "Address not found.")


class UserNotFoundException(AppException):
    def __init__(self):
        super().__init__(HTTPStatus.NOT_FOUND, "User not found.")


class UserEmailAlreadyExistsException(AppException):
    def __init__(self):
        super().__init__(HTTPStatus.CONFLICT, "Email already exists.")


class SamePasswordException(AppException): 
    def __init__(self):
        super().__init__(HTTPStatus.BAD_REQUEST, "New password must be different from the old one.")


class InvalidTokenException(AppException): 
    def __init__(self):
        super().__init__(HTTPStatus.UNAUTHORIZED, "Invalid token.")


class UnauthorizedException(AppException): 
    def __init__(self):
        super().__init__(HTTPStatus.UNAUTHORIZED, "Unauthorized access.")
