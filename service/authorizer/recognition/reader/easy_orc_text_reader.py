from easyocr import easyocr

from service.authorizer.recognition.detector.model.image import Image
from service.authorizer.recognition.reader.model.text_detection import TextDetection
from service.authorizer.recognition.reader.text_reader import TextReader


class EasyOcrTextReader(TextReader):
    def __init__(self):
        self.ocr = easyocr.Reader(['en'])

    def read(self, preprocessed_image: Image) -> list[TextDetection]:
        detections = self.ocr.readtext(preprocessed_image)

        text_detections = []
        for detection in detections:
            _, text, confidence = detection
            text = text.upper().replace(' ', '')
            text_detections.append(TextDetection(text, confidence))

        return text_detections
