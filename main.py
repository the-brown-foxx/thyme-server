from typing import Optional

from fastapi import FastAPI, status
from fastapi.responses import JSONResponse

from pydantic import BaseModel

from service.registry.actual_car_registry import ActualCarRegistry
from service.registry.car_registry import CarRegistry
from service.registry.model.exception import CarNotFoundError, FieldCannotBeBlankError, PasswordTooShortError, \
    RegistrationIdTakenError
from service.registry.repository.actual_car_repository import ActualCarRepository

app = FastAPI()

car_registry: CarRegistry = ActualCarRegistry(ActualCarRepository())


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
        status_code=status.HTTP_400_BAD_REQUEST,
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
async def car_not_found_exception_handler(_, exception: Exception):
    return JSONResponse(
        status_code=status.HTTP_404_NOT_FOUND,
        content={
            "status": "INTERNAL_SERVER_ERROR",
            "message": str(exception),
        },
    )


@app.get("/cars", status_code=status.HTTP_200_OK)
async def get_cars():
    return {
        "status": "SUCCESSFUL",
        "cars": car_registry.get_cars()
    }


@app.get("/cars/{registration_id}", status_code=status.HTTP_200_OK)
async def get_car(registration_id: str):
    return {
        "status": "SUCCESSFUL",
        "car": car_registry.get_car(registration_id),
    }


class NewCar(BaseModel):
    registration_id: str
    make: str
    model: str
    year: int
    owner: str


@app.post("/cars", status_code=status.HTTP_201_CREATED)
async def register_car(new_car: NewCar):
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
    owner: Optional[str] = None
    password: Optional[str] = None


@app.patch("/cars", status_code=status.HTTP_200_OK)
async def update_car(car_update: CarUpdate):
    car_registry.update_car(car_update)
    return {
        "status": "SUCCESSFUL",
        "message": "Car updated successfully",
    }


@app.delete("/cars/{registration_id}", status_code=status.HTTP_200_OK)
async def unregister_car(registration_id: str):
    car_registry.unregister_car(registration_id)
    return {
        "status": "SUCCESSFUL",
        "message": "Car unregistered successfully",
    }
