from peewee import DoesNotExist

from service.authenticator.log.model.car_log import CarLog
from service.authenticator.log.repository.car_log_repository import CarLogRepository
from service.authenticator.log.repository.car_log_entity import CarLogEntity


def log_entity_to_car_log(log_entity: CarLogEntity):
    return CarLog(
        date_time=log_entity.date_time,
        car_registration_id=log_entity.car_registration_id,
        entering=log_entity.entering,
        image=log_entity.image,
    )


def car_log_to_log_entity(car_log: CarLog):
    return CarLogEntity(
        date_time=car_log.date_time,
        entering=car_log.entering,
        image=car_log.image,
        car_registration_id=car_log.car_registration_id,
    )


class ActualCarLogRepository(CarLogRepository):
    CarLogEntity.create_table(safe=True)

    def get_logs(self) -> list[CarLog]:
        logs: list[CarLog] = []
        car_logs = CarLogEntity.select()

        for car_log in car_logs:
            logs.append(log_entity_to_car_log(car_log))

        return logs

    def get_logs_by_car_registration_id(self, registration_id: str) -> list[CarLog]:
        logs: list[CarLog] = []
        log_entities = CarLogEntity.select(CarLogEntity.car_registration_id == registration_id)

        for car_log in log_entities:
            logs.append(log_entity_to_car_log(car_log))
        return logs

    def upsert_log(self, car_log: CarLog):
        new_log_entity = car_log_to_log_entity(car_log)

        try:
            old_log_entity: CarLogEntity = CarLogEntity.get(CarLogEntity.log_id == new_log_entity.log_id)
            old_log_entity.car_registration_id = new_log_entity.car_registration_id
            old_log_entity.entering = new_log_entity.entering
            old_log_entity.image = new_log_entity.image
            old_log_entity.sus = new_log_entity.sus
            old_log_entity.save()
        except DoesNotExist:
            new_log_entity.save()

