from abc import ABC, abstractmethod

import cv2


class VideoStreamProvider(ABC):
    @abstractmethod
    def get_stream(self) -> cv2.VideoCapture:
        pass

    @abstractmethod
    def get_fps(self) -> int:
        pass
