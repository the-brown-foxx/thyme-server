from typing import Union

import cv2

from service.authorizer.stream.video_stream_provider import VideoStreamProvider


class SourceVideoStreamProvider(VideoStreamProvider):
    def __init__(self, source: Union[int, str], thresholds: list[int]):
        self.source = source
        self.thresholds = thresholds

    def get_stream(self) -> cv2.VideoCapture:
        return cv2.VideoCapture(self.source)

    def get_thresholds(self) -> list[int]:
        return self.thresholds
