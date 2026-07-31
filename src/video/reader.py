from dataclasses import dataclass
from pathlib import Path

import cv2


@dataclass
class VideoMetadata:
    """Store basic metadata of a video."""

    path: str
    fps: float
    width: int
    height: int
    frame_count: int
    duration_seconds: float


def read_video_metadata(video_path: str) -> VideoMetadata:
    """Read and return basic metadata from a video file."""

    path = Path(video_path)

    if not path.exists():
        raise FileNotFoundError(f"Video file not found: {video_path}")

    capture = cv2.VideoCapture(str(path))

    if not capture.isOpened():
        raise ValueError(f"Unable to open video file: {video_path}")

    fps = float(capture.get(cv2.CAP_PROP_FPS))
    width = int(capture.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(capture.get(cv2.CAP_PROP_FRAME_HEIGHT))
    frame_count = int(capture.get(cv2.CAP_PROP_FRAME_COUNT))

    capture.release()

    duration_seconds = frame_count / fps if fps > 0 else 0.0

    return VideoMetadata(
        path=str(path),
        fps=fps,
        width=width,
        height=height,
        frame_count=frame_count,
        duration_seconds=duration_seconds,
    )