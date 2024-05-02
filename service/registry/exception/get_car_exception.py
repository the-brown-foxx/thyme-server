class CarNotFound(Exception):

    registration_id: str

    def __init__(self, registration_id: str):
        self.registration_id = registration_id
        self.message = f"Car with registration ID {registration_id} is not in the registry"

    def __str__(self):
        return self.message
