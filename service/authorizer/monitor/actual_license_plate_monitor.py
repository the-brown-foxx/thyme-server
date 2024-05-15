from typing import Optional

import cv2
from reactivex import Observable, Subject
from easyocr import easyocr, Reader
from ultralytics import YOLO

from service.authorizer.format.registration_id_format import RegistrationIdFormat
from service.authorizer.monitor.license_plate_monitor import LicensePlateMonitor
from service.authorizer.stream.video_stream_provider import VideoStreamProvider


def preprocess_license_plate(license_plate):
    if license_plate is not None:
        gray_license_plate = cv2.cvtColor(license_plate, cv2.COLOR_BGR2GRAY)
        _, black_white_license_plate = cv2.threshold(gray_license_plate, 64, 255, cv2.THRESH_BINARY_INV)


def annotate_frame(frame, text):
    cv2.putText(frame, text, (0, 0), cv2.FONT_HERSHEY_PLAIN, 1, (255, 0, 0))


# TODO: Handle error correction and find a way to not check partially obstructed plate numbers
class ActualLicensePlateMonitor(LicensePlateMonitor):
    model: YOLO
    ocr: Reader

    video_stream_provider: VideoStreamProvider
    registration_id_format: RegistrationIdFormat

    old_registration_id: Optional[str]
    registration_id_stream: Subject[str]()

    def __init__(
            self,
            video_stream_provider: VideoStreamProvider,
            registration_id_format: RegistrationIdFormat,
            headless: bool = True,
    ):
        self.model = YOLO('service/authorizer/monitor/license_plate_detector.pt')
        self.ocr = easyocr.Reader(['en'])

        self.video_stream_provider = video_stream_provider
        self.registration_id_format = registration_id_format

        self.old_registration_id = None
        self.registration_id_stream = Subject()
        self.start(headless)

    def crop_license_plate(self, frame):
        license_plates = self.model(frame)[0]
        try:
            license_plate = license_plates.boxes.data.tolist()[0]
            x1, y1, x2, y2, score, class_id = license_plate
            return frame[int(y1):int(y2), int(x1):int(x2), :]
        except IndexError:
            return None

    def read_license_plate(self, preprocessed_license_plate) -> Optional[str]:
        if preprocessed_license_plate is not None:
            detections = self.ocr.readtext(preprocessed_license_plate)

            for detection in detections:
                _, text, _ = detection
                text = text.upper().replace(' ', '')
                return text
        else:
            return None

    def start(self, headless: bool = True):
        video_stream = self.video_stream_provider.get_stream()

        while video_stream.isOpened():
            success, frame = video_stream.read()

            if success:
                license_plate = self.crop_license_plate(frame)
                preprocess_license_plate(license_plate)
                registration_id = self.read_license_plate(license_plate)

                if registration_id is not None:
                    if not headless:
                        annotate_frame(frame, registration_id)
                        print(registration_id)
                        cv2.imshow("YOLOv8 Inference", frame)

                    if self.registration_id_format.valid(registration_id):
                        self.registration_id_stream.on_next(registration_id)

                if not headless:
                    cv2.imshow("YOLOv8 Inference", frame)

                if cv2.waitKey(1) & 0xFF == ord("q"):
                    break

            else:
                break

    def get_registration_id_stream(self) -> Observable[str]:
        return self.registration_id_stream
