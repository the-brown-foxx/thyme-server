from abc import ABC, abstractmethod

import cv2


class VideoStreamProvider(ABC):
    @abstractmethod
    def get_stream(self, video_id: str) -> cv2.VideoCapture:
        pass
