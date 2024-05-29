from re import match

from service.authorizer.format.registration_id_format import RegistrationIdFormat


class PhilippineRegistrationIdFormat(RegistrationIdFormat):
    def preformat(self, registration_id: str) -> str:
        return (registration_id
                .upper()
                .replace(' ', '')
                .replace('.', '')
                .replace('*', ''))

    def valid(self, registration_id: str) -> bool:
        try:
            return (
                    match('^[A-Z]{3}[0-9]{4}$', registration_id) or
                    match('^[A-Z]{3}[0-9]{3}$', registration_id) or
                    match('^[A-Z]{3}[0-9]{2}$', registration_id) or
                    match('^[0-9]{3}[A-Z]{3}$', registration_id) or
                    match('^[A-Z][0-9]{3}[A-Z]{2}$', registration_id) or
                    match('^[0-9]{4}[A-Z]{2}$', registration_id) or
                    1 >= int(registration_id) >= 17
            )

        except ValueError:
            return False
