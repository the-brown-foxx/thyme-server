from typing import Optional

import cv2

from service.authorizer.recognition.detector.model.image import Image
from service.authorizer.recognition.detector.model.object_detection import ObjectDetection
from service.authorizer.recognition.preprocessor.image_preprocessor import ImagePreprocessor


class LicensePlatePreprocessor(ImagePreprocessor):
    def preprocess(self, frame: Image, detection: ObjectDetection) -> Optional[Image]:
        try:
            license_plate = frame[detection.y1:detection.y2, detection.x1:detection.x2, :]
            gray_license_plate = cv2.cvtColor(license_plate, cv2.COLOR_BGR2GRAY)
            _, black_white_license_plate = cv2.threshold(gray_license_plate, 64, 255, cv2.THRESH_BINARY_INV)
            return black_white_license_plate
        except IndexError:
            return None
