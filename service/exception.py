from constants import min_password_length


class CarNotFoundError(Exception):
    registration_id: str
    message: str

    def __init__(self, registration_id: str):
        self.registration_id = registration_id
        self.message = f"Car with registration ID {registration_id} is not in the registry"

    def __str__(self):
        return self.message


class RegistrationIdTakenError(Exception):
    registration_id: str
    message: str

    def __init__(self, registration_id: str):
        self.registration_id = registration_id
        self.message = f"Registration ID {registration_id} is already taken"

    def __str__(self):
        return self.message


class FieldCannotBeBlankError(Exception):
    field_name: str
    message: str

    def __init__(self, field_name: str):
        self.field_name = field_name
        self.message = f"Field {field_name} cannot be blank"

    def __str__(self):
        return self.message


class PasswordTooShortError(Exception):
    min_length: int = min_password_length
    message: str

    def __init__(self):
        self.message = f"Password must be at least {self.min_length} characters long"

    def __str__(self):
        return self.message


class IncorrectPasswordError(Exception):
    message: str

    def __init__(self):
        self.message = "Incorrect password"

    def __str__(self):
        return self.message


class InvalidTokenError(Exception):
    message: str

    def __init__(self):
        self.message = "Invalid token"

    def __str__(self):
        return self.message


class CarNotAuthorizedException(Exception):
    message: str
    registration_id: str

    def __init__(self, registration_id: str):
        self.registration_id = registration_id
        self.message = f"Car with registration ID {registration_id} is not authorized"
