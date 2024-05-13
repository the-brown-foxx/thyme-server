from service.authorizer.format.registration_id_format import RegistrationIdFormat


class AnyRegistrationIdFormat(RegistrationIdFormat):
    def valid(self, registration_id: str):
        return True
