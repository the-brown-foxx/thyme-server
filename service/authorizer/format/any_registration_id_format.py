from service.authorizer.format.registration_id_format import RegistrationIdFormat


class AnyRegistrationIdFormat(RegistrationIdFormat):
    def preformat(self, registration_id: str) -> str:
        return ''.join(filter(lambda char: char.isalnum(), registration_id))

    def valid(self, registration_id: str) -> bool:
        return True
