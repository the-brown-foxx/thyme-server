from threading import Thread

import cv2
from reactivex import Subject, Observable

from service.authorizer.monitor.license.license_plate_monitor import LicensePlateMonitor
from service.authorizer.monitor.model.car_snapshot import CarSnapshot
from service.authorizer.recognition.corrector.text_corrector import TextCorrector
from service.authorizer.recognition.detector.model.image import Image
from service.authorizer.recognition.detector.model.object_detection import ObjectDetection
from service.authorizer.recognition.detector.object_detector import ObjectDetector
from service.authorizer.recognition.preprocessor.image_preprocessor import ImagePreprocessor
from service.authorizer.recognition.reader.text_reader import TextReader
from service.authorizer.stream.video_stream_provider import VideoStreamProvider


class ModularLicensePlateMonitor(LicensePlateMonitor):
    def __init__(
            self,
            name: str,
            video_stream_provider: VideoStreamProvider,
            license_plate_detector: ObjectDetector,
            license_plate_preprocessor: ImagePreprocessor,
            registration_id_reader: TextReader,
            text_corrector: TextCorrector,
    ):
        self.name = name
        self.video_stream_provider = video_stream_provider
        self.car_snapshots = Subject[CarSnapshot]()
        self.license_plate_detector = license_plate_detector
        self.license_plate_preprocessor = license_plate_preprocessor
        self.license_plate_reader = registration_id_reader
        self.text_corrector = text_corrector

        self.thread = Thread(target=self._start)
        self.thread.start()

    def get_registration_id_stream(self) -> Observable[CarSnapshot]:
        return self.car_snapshots

    def get_thread(self) -> Thread:
        return self.thread

    def _start(self):
        video_stream = self.video_stream_provider.get_stream()

        while video_stream.isOpened():
            successful, frame = video_stream.read()

            if not successful:
                break

            self._read_frame(frame)

            if cv2.waitKey(1) & 0xFF == ord("q"):
                break

    def _read_frame(self, frame: Image):
        cv2.imshow(f'Camera [{self.name}]', frame)
        license_plate_detection = self.license_plate_detector.detect_object(frame)
        if license_plate_detection is None:
            return

        for threshold in self.video_stream_provider.get_thresholds():
            self._read_at_threshold(frame, license_plate_detection, threshold)

    def _read_at_threshold(self, frame: Image, license_plate_detection: ObjectDetection, threshold: int):
        preprocessed_license_plate = self.license_plate_preprocessor.preprocess(
            frame,
            license_plate_detection,
            threshold,
        )
        if preprocessed_license_plate is not None:
            cv2.imshow(f'License Plate Monitor [{self.name} T-{threshold}]', preprocessed_license_plate)
            registration_id_detections = self.license_plate_reader.read(preprocessed_license_plate)

            # Concatenate the second detection in case the plate was cut in the middle
            if len(registration_id_detections) >= 1:
                self._emit_snapshot(registration_id_detections[0].value, frame)
            if len(registration_id_detections) >= 2:
                self._emit_snapshot(registration_id_detections[0].value + registration_id_detections[1].value, frame)

    def _emit_snapshot(self, registration_id: str, frame: Image):
        possible_registration_ids = self.text_corrector.get_possible_texts(registration_id)
        for possible_registration_id in possible_registration_ids:
            self.car_snapshots.on_next(CarSnapshot(possible_registration_id, frame))
