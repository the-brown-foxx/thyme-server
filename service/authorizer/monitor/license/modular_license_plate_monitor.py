from threading import Thread

import cv2
from reactivex import Subject, Observable

from service.authorizer.monitor.license.license_plate_monitor import LicensePlateMonitor
from service.authorizer.recognition.detector.model.image import Image
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
    ):
        self.name = name
        self.video_stream_provider = video_stream_provider
        self.registration_id_stream = Subject[str]()
        self.license_plate_detector = license_plate_detector
        self.license_plate_preprocessor = license_plate_preprocessor
        self.license_plate_reader = registration_id_reader

        self.thread = Thread(target=self._start)
        self.thread.start()

    def get_registration_id_stream(self) -> Observable[str]:
        return self.registration_id_stream

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

        preprocessed_license_plate = self.license_plate_preprocessor.preprocess(frame, license_plate_detection)
        if preprocessed_license_plate is None:
            return

        registration_id_detection = self.license_plate_reader.read(preprocessed_license_plate)

        if registration_id_detection is not None:
            self.registration_id_stream.on_next(registration_id_detection.value)
            print(registration_id_detection)
            cv2.imshow(f'License Plate Monitor [{self.name}]', preprocessed_license_plate)
            cv2.putText(frame, registration_id_detection.value, (0, 0), cv2.FONT_HERSHEY_PLAIN, 1, (255, 0, 0))
