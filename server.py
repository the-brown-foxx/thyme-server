from typing import Optional, Annotated

from fastapi import FastAPI, WebSocket, status, Depends
from fastapi.responses import JSONResponse
from fastapi.security import OAuth2PasswordBearer
from pydantic import BaseModel

from service.authenticator.admin.actual_admin_authenticator import ActualAdminAuthenticator
from service.authenticator.admin.admin_authenticator import AdminAuthenticator
from service.authenticator.admin.repository.actual_admin_password_repository import ActualAdminPasswordRepository
from service.authenticator.token.actual_token_processor import ActualTokenProcessor
from service.connection.websocket_manager import WebsocketManager
from service.exception import RegistrationIdTakenError, FieldCannotBeBlankError, PasswordTooShortError
from service.registry.actual_car_registry import ActualCarRegistry
from service.registry.car_registry import CarRegistry
from service.registry.repository.actual_car_repository import ActualCarRepository
from sockets.car_registry import handle_car_registry_websocket

app = FastAPI()

oauth_scheme = OAuth2PasswordBearer(tokenUrl="token")

admin_authenticator: AdminAuthenticator = ActualAdminAuthenticator(
    ActualAdminPasswordRepository(),
    ActualTokenProcessor(),
)

car_registry_websocket_manager = WebsocketManager(admin_authenticator)

car_registry: CarRegistry = ActualCarRegistry(ActualCarRepository())


class Password(BaseModel):
    password: str


class PasswordChange(BaseModel):
    old_password: Optional[str] = None
    new_password: str


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


@app.post("/admin/login", status_code=status.HTTP_200_OK)
async def login(password: Password):
    return {
        "status": "SUCCESSFUL",
        "token": admin_authenticator.login(password.password),
    }


@app.post("/admin/change-password", status_code=status.HTTP_200_OK)
async def change_password(password_change: PasswordChange):
    admin_authenticator.change_password(password_change.old_password, password_change.new_password)
    return {
        "status": "SUCCESSFUL",
        "message": "Password changed successfully",
    }


@app.websocket('/car-registry')
async def car_registry_websocket(websocket: WebSocket):
    await handle_car_registry_websocket(car_registry_websocket_manager, car_registry, websocket)
