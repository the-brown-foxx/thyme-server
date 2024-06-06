import cv2

from service.authorizer.stream.video_stream_provider import VideoStreamProvider


class SourceVideoStreamProvider(VideoStreamProvider):
    source: int | str

    def __init__(self, source: int | str):
        self.source = source

    def get_stream(self) -> cv2.VideoCapture:
        return cv2.VideoCapture(self.source)

    def get_fps(self) -> int:
        return 30
