import cv2

from service.authorizer.stream.video_stream_provider import VideoStreamProvider


class DummyVideoStreamProvider(VideoStreamProvider):
    def get_stream(self) -> cv2.VideoCapture:
        return cv2.VideoCapture("dummy_video_stream.mp4")
