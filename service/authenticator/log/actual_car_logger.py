from dataclasses import replace
from datetime import datetime

import cv2

from service.authenticator.log.car_logger import CarLogger
from service.authenticator.log.model.car_log import CarLog
from service.authenticator.log.repository.car_log_repository import CarLogRepository
from service.authorizer.stream.video_stream_provider import VideoStreamProvider


class ActualCarLogger(CarLogger):
    log_repository: CarLogRepository
    video_stream_provider: VideoStreamProvider

    def __init__(self, log_repository: CarLogRepository, video_steam_provider: VideoStreamProvider):
        self.log_repository = log_repository
        self.video_stream_provider = video_steam_provider

    def get_logs(self) -> list[CarLog]:
        return self.log_repository.get_logs()

    def get_logs_by_car_registration_id(self, car_registration_id: str) -> list[CarLog]:
        return self.log_repository.get_logs_by_car_registration_id(car_registration_id)

    def log(self, car_registration_id: str, entering: bool):
        _, image_frame = self.video_stream_provider.get_stream().read()
        date_time = datetime.now()
        filename = f'LOG_{date_time.strftime('%d%m%y_%H%M%S_%f')}'
        cv2.imwrite(filename, image_frame)

        sus_tracker = sorted(
            self.get_logs_by_car_registration_id(car_registration_id),
            key=lambda element: element.date_time,
        )

        if len(sus_tracker) > 0:
            last = sus_tracker[len(sus_tracker) - 1]
            sus = last.entering
            log = CarLog(
                date_time=date_time,
                car_registration_id=car_registration_id,
                entering=entering,
                image=filename,
                sus=sus,
            )
            self.log_repository.upsert_log(log)

            if sus:
                new_last = replace(last, sus=True)
                self.log_repository.upsert_log(new_last)

        else:
            log = CarLog(
                date_time=date_time,
                car_registration_id=car_registration_id,
                entering=entering,
                image=filename,
                sus=False,
            )
            self.log_repository.upsert_log(log)
