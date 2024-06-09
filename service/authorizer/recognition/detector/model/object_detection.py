from dataclasses import dataclass


@dataclass
class ObjectDetection:
    x1: int
    y1: int
    x2: int
    y2: int
    confidence: float
