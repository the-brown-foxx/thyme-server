from abc import ABC, abstractmethod
from typing import Optional

from service.authorizer.recognition.detector.model.object_detection import ObjectDetection
from service.authorizer.recognition.detector.model.image import Image


class ImagePreprocessor(ABC):
    @abstractmethod
    def preprocess(self, frame: Image, detection: ObjectDetection) -> Optional[Image]:
        pass
