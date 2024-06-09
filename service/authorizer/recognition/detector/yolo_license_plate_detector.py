from typing import Optional

from ultralytics import YOLO

from service.authorizer.recognition.detector.object_detector import ObjectDetector
from service.authorizer.recognition.detector.model.image import Image
from service.authorizer.recognition.detector.model.object_detection import ObjectDetection


class YoloLicensePlateDetector(ObjectDetector):
    def __init__(self):
        self.model = YOLO('service/authorizer/monitor/license/license_plate_detector.pt')

    def detect_object(self, frame: Image) -> Optional[ObjectDetection]:
        license_plates = self.model(frame, verbose=False)[0]
        try:
            license_plate = license_plates.boxes.data.tolist()[0]
            x1, y1, x2, y2, score, _ = license_plate
            return ObjectDetection(int(x1), int(y1), int(x2), int(y2), score)
        except IndexError:
            return None
