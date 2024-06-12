from dataclasses import replace
from datetime import datetime

import cv2
from reactivex import Subject, Observable
from reactivex.subject import BehaviorSubject

from service.authorizer.log.car_logger import CarLogger
from service.authorizer.log.model.car_log import CarLog
from service.authorizer.log.repository.car_log_repository import CarLogRepository
from service.authorizer.monitor.model.car_snapshot import CarSnapshot


class ActualCarLogger(CarLogger):
    log_repository: CarLogRepository

    logs: Subject[list[CarLog]]

    def __init__(
            self,
            log_repository: CarLogRepository,
            # video_steam_provider: VideoStreamProvider,
    ):
        self.log_repository = log_repository
        self.logs = BehaviorSubject(self.get_logs())
        # self.video_stream_provider = video_steam_provider

    def update_live_logs(self):
        self.logs.on_next(self.get_logs())

    def get_live_logs(self) -> Observable[list[CarLog]]:
        return self.logs

    def get_logs(self) -> list[CarLog]:
        return self.log_repository.get_logs()

    def get_logs_by_car_registration_id(self, car_registration_id: str) -> list[CarLog]:
        return self.log_repository.get_logs_by_car_registration_id(car_registration_id)

    def log(self, car_snapshot: CarSnapshot, entering: bool):
        print('Logged')
        date_time = datetime.now()
        filename = f'LOG_{date_time.strftime('%d%m%y_%H%M%S_%f')}.jpg'
        cv2.imwrite(f'snapshots/{filename}', car_snapshot.snapshot)

        sus_tracker = sorted(
            self.get_logs_by_car_registration_id(car_snapshot.registration_id),
            key=lambda element: element.date_time,
        )

        if entering and len(sus_tracker) > 0:
            last = sus_tracker[len(sus_tracker) - 1]
            sus = last.entering
            log = CarLog(
                date_time=date_time,
                car_registration_id=car_snapshot.registration_id,
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
                car_registration_id=car_snapshot.registration_id,
                entering=entering,
                image=filename,
                sus=False,
            )
            self.log_repository.upsert_log(log)

        self.update_live_logs()
