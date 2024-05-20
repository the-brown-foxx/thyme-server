import cv2

from service.authorizer.stream.video_stream_provider import VideoStreamProvider


class WebcamVideoStreamProvider(VideoStreamProvider):
    def get_stream(self) -> cv2.VideoCapture:
        return cv2.VideoCapture(0)

    def get_fps(self) -> int:
        return 30
