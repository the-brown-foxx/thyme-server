from typing import Optional

from reactivex import Observable, Subject

from service.authorizer.filter.registration_id_filter import RegistrationIdFilter
from service.authorizer.format.registration_id_format import RegistrationIdFormat


class ScoringRegistrationIdFilter(RegistrationIdFilter):
    target_score = 10

    last_registration_id: Optional[str]
    registration_id_format: RegistrationIdFormat
    registration_ids: Observable[str]

    filtered_registration_ids: Subject[str]
    scores: dict[str, int]

    def __init__(self, registration_id_format: RegistrationIdFormat):
        self.registration_id_format = registration_id_format

    def get_filtered_stream(self, registration_ids: Observable[str]) -> Observable[str]:
        self.registration_ids = registration_ids
        self.registration_ids.subscribe(lambda registration_id: self.on_next(registration_id))
        self.filtered_registration_ids = Subject()
        self.scores = {}
        self.last_registration_id = None
        return self.filtered_registration_ids

    def on_next(self, registration_id):
        registration_id = self.registration_id_format.preformat(registration_id)
        if not self.registration_id_format.valid(registration_id):
            return

        self.scores[registration_id] = self.scores.get(registration_id, 0) + 1

        if self.scores[registration_id] >= self.target_score:
            self.scores = {}

            if self.last_registration_id is None or registration_id not in self.last_registration_id:
                self.filtered_registration_ids.on_next(registration_id)
                self.last_registration_id = registration_id
