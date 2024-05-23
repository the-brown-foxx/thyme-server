from typing import Optional, Annotated

from fastapi import FastAPI, status, Depends
from fastapi.responses import JSONResponse
from fastapi.security import OAuth2PasswordBearer

from pydantic import BaseModel

from service.authenticator.admin.actual_admin_authenticator import ActualAdminAuthenticator
from service.authenticator.admin.admin_authenticator import AdminAuthenticator
from service.authenticator.admin.repository.actual_admin_password_repository import ActualAdminPasswordRepository
from service.authorizer.log.actual_car_logger import ActualCarLogger
from service.authorizer.log.car_logger import CarLogger
from service.authorizer.log.repository.actual_car_log_repository import ActualCarLogRepository
from service.authenticator.token.actual_token_processor import ActualTokenProcessor
from service.authorizer.stream.webcam_video_stream_provider import WebcamVideoStreamProvider
from service.registry.actual_car_registry import ActualCarRegistry
from service.registry.car_registry import CarRegistry
from service.exception import CarNotFoundError, FieldCannotBeBlankError, PasswordTooShortError, \
    RegistrationIdTakenError, IncorrectPasswordError, InvalidTokenError
from service.registry.repository.actual_car_repository import ActualCarRepository

app = FastAPI()

admin_authenticator: AdminAuthenticator = ActualAdminAuthenticator(
    ActualAdminPasswordRepository(),
    ActualTokenProcessor(),
)

car_registry: CarRegistry = ActualCarRegistry(ActualCarRepository())
car_logger: CarLogger = ActualCarLogger(ActualCarLogRepository(), WebcamVideoStreamProvider())
oauth_scheme = OAuth2PasswordBearer(tokenUrl="token")


@app.exception_handler(CarNotFoundError)
async def car_not_found_exception_handler(_, exception: CarNotFoundError):
    return JSONResponse(
        status_code=status.HTTP_404_NOT_FOUND,
        content={
            "status": "CAR_NOT_FOUND",
            "registration_id": exception.registration_id,
            "message": exception.message,
        },
    )


@app.exception_handler(RegistrationIdTakenError)
async def registration_id_taken_exception_handler(_, exception: RegistrationIdTakenError):
    return JSONResponse(
        status_code=status.HTTP_409_CONFLICT,
        content={
            "status": "REGISTRATION_ID_TAKEN",
            "registration_id": exception.registration_id,
            "message": exception.message,
        },
    )


@app.exception_handler(FieldCannotBeBlankError)
async def field_cannot_be_blank_exception_handler(_, exception: FieldCannotBeBlankError):
    return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST,
        content={
            "status": "FIELD_CANNOT_BE_BLANK",
            "field_name": exception.field_name,
            "message": exception.message,
        },
    )


@app.exception_handler(PasswordTooShortError)
async def password_too_short_exception_handler(_, exception: PasswordTooShortError):
    return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST,
        content={
            "status": "PASSWORD_TOO_SHORT",
            "min_length": exception.min_length,
            "message": exception.message,
        },
    )


@app.exception_handler(IncorrectPasswordError)
async def incorrect_password_exception_handler(_, exception: IncorrectPasswordError):
    return JSONResponse(
        status_code=status.HTTP_401_UNAUTHORIZED,
        content={
            "status": "INCORRECT_PASSWORD",
            "message": exception.message,
        },
    )


@app.exception_handler(InvalidTokenError)
async def invalid_token_exception_handler(_, exception: InvalidTokenError):
    return JSONResponse(
        status_code=status.HTTP_401_UNAUTHORIZED,
        content={
            "status": "INVALID_TOKEN",
            "message": exception.message,
        },
    )


@app.exception_handler(Exception)
async def internal_server_error_handler(_, exception: Exception):
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={
            "status": "INTERNAL_SERVER_ERROR",
            "message": str(exception),
        },
    )


@app.get("/admin/password-set", status_code=status.HTTP_200_OK)
async def password_set():
    return {
        "status": "SUCCESSFUL",
        "password_set": admin_authenticator.password_set(),
    }


class Password(BaseModel):
    password: str


@app.post("/admin/login", status_code=status.HTTP_200_OK)
async def login(password: Password):
    return {
        "status": "SUCCESSFUL",
        "token": admin_authenticator.login(password.password),
    }


class PasswordChange(BaseModel):
    old_password: Optional[str] = None
    new_password: str


@app.post("/admin/change-password", status_code=status.HTTP_200_OK)
async def change_password(password_change: PasswordChange):
    admin_authenticator.change_password(password_change.old_password, password_change.new_password)
    return {
        "status": "SUCCESSFUL",
        "message": "Password changed successfully",
    }


@app.get("/cars", status_code=status.HTTP_200_OK)
async def get_cars(token: Annotated[str, Depends(oauth_scheme)]):
    admin_authenticator.require_authentication(token)
    return {
        "status": "SUCCESSFUL",
        "cars": car_registry.get_cars()
    }


@app.get("/cars/{registration_id}", status_code=status.HTTP_200_OK)
async def get_car(token: Annotated[str, Depends(oauth_scheme)], registration_id: str):
    admin_authenticator.require_authentication(token)
    return {
        "status": "SUCCESSFUL",
        "car": car_registry.get_car(registration_id),
    }


class NewCar(BaseModel):
    registration_id: str
    make: str
    model: str
    year: int
    color: str
    owner: str


@app.post("/cars", status_code=status.HTTP_201_CREATED)
async def register_car(token: Annotated[str, Depends(oauth_scheme)], new_car: NewCar):
    admin_authenticator.require_authentication(token)
    car_registry.register_car(new_car)
    return {
        "status": "SUCCESSFUL",
        "message": "Car registered successfully",
    }


class CarUpdate(BaseModel):
    registration_id: str
    make: Optional[str] = None
    model: Optional[str] = None
    year: Optional[int] = None
    color: Optional[str] = None
    owner: Optional[str] = None
    password: Optional[str] = None


@app.patch("/cars", status_code=status.HTTP_200_OK)
async def update_car(token: Annotated[str, Depends(oauth_scheme)], car_update: CarUpdate):
    admin_authenticator.require_authentication(token)
    car_registry.update_car(car_update)
    return {
        "status": "SUCCESSFUL",
        "message": "Car updated successfully",
    }


@app.delete("/cars/{registration_id}", status_code=status.HTTP_200_OK)
async def unregister_car(token: Annotated[str, Depends(oauth_scheme)], registration_id: str):
    admin_authenticator.require_authentication(token)
    car_registry.unregister_car(registration_id)
    return {
        "status": "SUCCESSFUL",
        "message": "Car unregistered successfully",
    }


@app.get("/logs", status_code=status.HTTP_200_OK)
async def get_logs(token: Annotated[str, Depends(oauth_scheme)]):
    admin_authenticator.require_authentication(token)
    return {
        "status": "SUCCESSFUL",
        "logs": car_logger.get_logs(),
    }


@app.get("/logs/{registration_id}", status_code=status.HTTP_200_OK)
async def get_log(token: Annotated[str, Depends(oauth_scheme)], registration_id: str):
    admin_authenticator.require_authentication(token)
    return {
        "status": "SUCCESSFUL",
        "logs": car_logger.get_logs_by_car_registration_id(registration_id),
    }
