class CarNotFoundError(Exception):

    registration_id: str

    def __init__(self, registration_id: str):
        self.registration_id = registration_id
        self.message = f"Car with registration ID {registration_id} is not in the registry"

    def __str__(self):
        return self.message


class FieldCannotBeBlankError(Exception):

    field_name: str

    def __init__(self, field_name: str):
        self.field_name = field_name
        self.message = f"Field {field_name} cannot be blank"

    def __str__(self):
        return self.message
