from dataclasses import dataclass
from pathlib import Path

import cv2

from src.motion.frame_difference import (
    FrameAnalysis,
    calculate_brightness_change,
    calculate_brightness_normalized_difference,
    calculate_frame_difference,
)


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
def count_readable_frames(video_path: str) -> int:
    """Read the video frame by frame and count readable frames."""

    path = Path(video_path)

    if not path.exists():
        raise FileNotFoundError(f"Video file not found: {video_path}")

    capture = cv2.VideoCapture(str(path))

    if not capture.isOpened():
        raise ValueError(f"Unable to open video file: {video_path}")

    readable_frame_count = 0

    while True:
        success, _ = capture.read()

        if not success:
            break

        readable_frame_count += 1

    capture.release()

    return readable_frame_count


def analyze_video_frames(
    video_path: str,
) -> list[FrameAnalysis]:
    """Calculate frame difference scores for an entire video."""

    path = Path(video_path)

    if not path.exists():
        raise FileNotFoundError(f"Video file not found: {video_path}")

    capture = cv2.VideoCapture(str(path))

    if not capture.isOpened():
        raise ValueError(f"Unable to open video file: {video_path}")

    success, previous_frame = capture.read()

    if not success:
        capture.release()
        raise ValueError(f"Unable to read the first frame: {video_path}")

    analysis_results: list[FrameAnalysis] = []
    frame_number = 2

    while True:
        success, current_frame = capture.read()

        if not success:
            break

        frame_change_score = calculate_frame_difference(
            previous_frame,
            current_frame,
        )

        brightness_change = calculate_brightness_change(
            previous_frame,
            current_frame,
        )

        brightness_normalized_change = (
            calculate_brightness_normalized_difference(
                previous_frame,
                current_frame,
            )
        )

        analysis_results.append(
            FrameAnalysis(
                frame_number=frame_number,
                frame_change_score=frame_change_score,
                brightness_change=brightness_change,
                brightness_normalized_change=brightness_normalized_change,
            )
        )

        previous_frame = current_frame
        frame_number += 1

    capture.release()

    return analysis_results

def read_frame_pair(
    video_path: str,
    current_frame_number: int,
) -> tuple:
    """Read the previous and current frames at a specified frame number."""

    path = Path(video_path)

    if not path.exists():
        raise FileNotFoundError(f"Video file not found: {video_path}")

    if current_frame_number < 2:
        raise ValueError("Current frame number must be at least 2.")

    capture = cv2.VideoCapture(str(path))

    if not capture.isOpened():
        raise ValueError(f"Unable to open video file: {video_path}")

    previous_frame = None
    current_frame = None
    frame_number = 0

    while frame_number < current_frame_number:
        success, frame = capture.read()

        if not success:
            capture.release()
            raise ValueError(
                f"Unable to read frame pair ending at frame {current_frame_number}."
            )

        frame_number += 1

        if frame_number == current_frame_number - 1:
            previous_frame = frame

        if frame_number == current_frame_number:
            current_frame = frame
            break

    capture.release()

    if previous_frame is None or current_frame is None:
        raise ValueError(
            f"Unable to read frame pair ending at frame {current_frame_number}."
        )

    return previous_frame, current_frame