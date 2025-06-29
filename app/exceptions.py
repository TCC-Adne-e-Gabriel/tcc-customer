from typing import Any

class InvalidPasswordException(Exception): 
    pass

class AddressNotFoundException(Exception): 
    pass

class UserNotFoundException(Exception):
    pass

class UserEmailAlreadyExistsException(Exception):
    pass

class SamePasswordException(Exception): 
    pass

class InvalidTokenException(Exception): 
    pass
