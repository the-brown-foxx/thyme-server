from abc import ABC, abstractmethod
from typing import Optional

from service.authorizer.recognition.detector.model.object_detection import ObjectDetection
from service.authorizer.recognition.detector.model.image import Image


class ObjectDetector(ABC):
    @abstractmethod
    def detect_object(self, frame: Image) -> Optional[ObjectDetection]:
        pass
