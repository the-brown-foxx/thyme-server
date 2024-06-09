from abc import ABC, abstractmethod
from typing import Optional

from service.authorizer.recognition.detector.model.image import Image
from service.authorizer.recognition.reader.model.text_detection import TextDetection


class TextReader(ABC):
    @abstractmethod
    def read(self, preprocessed_image: Image) -> Optional[TextDetection]:
        pass
