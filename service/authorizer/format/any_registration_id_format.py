from service.authorizer.format.registration_id_format import RegistrationIdFormat


class AnyRegistrationIdFormat(RegistrationIdFormat):
    def preformat(self, registration_id: str):
        return (registration_id
                .replace(' ', '')
                .replace('.', '')
                .replace('*', ''))

    def valid(self, registration_id: str):
        return True
