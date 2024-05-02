from fastapi import FastAPI, status

from service.registry.actual_car_registry import ActualCarRegistry
from service.registry.car_registry import CarRegistry
from service.registry.exception.get_car_exception import CarNotFound
from service.registry.repository.dummy_car_repository import DummyCarRepository

app = FastAPI()


car_registry: CarRegistry = ActualCarRegistry(DummyCarRepository()) # TODO: replace this with the actual


@app.get("/cars", status_code=status.HTTP_200_OK)
async def get_cars():
    return {
        "status": "SUCCESSFUL",
        "cars": car_registry.get_cars()
    }


@app.get("/cars/{registration_id}", status_code=status.HTTP_200_OK)
async def get_car(registration_id: str):
    try:
        return {
            "status": "SUCCESSFUL",
            "car": car_registry.get_car(registration_id),
        }
    except CarNotFound as exception:
        return {
            "status": "CAR_NOT_FOUND",
            "registration_id": exception.registration_id,
            "message": exception.message,
        }

# TODO: define all the other endpoints
