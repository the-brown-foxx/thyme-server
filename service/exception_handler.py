from typing import Callable, Optional

from service.exception import *


def handle_exception(task: Callable) -> Optional[dict]:
    try:
        task()
        return None

    except CarNotFoundError as exception:
        return {
            "status": "REGISTRATION_ID_TAKEN",
            "registration_id": exception.registration_id,
            "message": exception.message,
        }

    except RegistrationIdTakenError as exception:
        return {
            "status": "REGISTRATION_ID_TAKEN",
            "registration_id": exception.registration_id,
            "message": exception.message,
        }

    except FieldCannotBeBlankError as exception:
        return {
            "status": "FIELD_CANNOT_BE_BLANK",
            "field_name": exception.field_name,
            "message": exception.message,
        }

    except PasswordTooShortError as exception:
        return {
            "status": "PASSWORD_TOO_SHORT",
            "min_length": exception.min_length,
            "message": exception.message,
        }

    except IncorrectPasswordError as exception:
        return {
            "status": "INCORRECT_PASSWORD",
            "message": exception.message,
        }

    except InvalidTokenError as exception:
        return {
            "status": "INVALID_TOKEN",
            "message": exception.message,
        }

    except UnsetParkingSpaceError as exception:
        return {
            "status": "UNSET_PARKING_SPACE",
            "message": str(exception),
        }

    except TotalSpaceIsLessThanVacantSpaceError as exception:
        return {
            "status": "TOTAL_SPACE_LESS_THAN_VACANT_SPACE",
            "message": str(exception),
        }

    except Exception as exception:
        return {
            "status": "INTERNAL_SERVER_ERROR",
            "message": str(exception),
        }
