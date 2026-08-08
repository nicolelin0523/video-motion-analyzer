from dataclasses import dataclass
from pathlib import Path

import cv2
import numpy as np
import pandas as pd
from numpy.typing import NDArray


@dataclass
class FrameAnalysis:
    """Store analysis results for one frame pair."""

    frame_number: int
    frame_change_score: float
    brightness_change: float
    brightness_normalized_change: float

def calculate_frame_difference(
    previous_frame: NDArray[np.uint8],
    current_frame: NDArray[np.uint8],
) -> float:
    """Calculate the average pixel difference between two video frames."""

    previous_gray = cv2.cvtColor(previous_frame, cv2.COLOR_BGR2GRAY)
    current_gray = cv2.cvtColor(current_frame, cv2.COLOR_BGR2GRAY)

    difference = cv2.absdiff(previous_gray, current_gray)
    difference_score = float(np.mean(difference))

    return difference_score

def save_analysis_results_to_csv(
    analysis_results: list[FrameAnalysis],
    fps: float,
    output_path: str,
) -> None:
    """Save frame analysis results and timestamps to a CSV file."""

    output = Path(output_path)
    output.parent.mkdir(parents=True, exist_ok=True)

    rows = []

    for result in analysis_results:
        time_seconds = result.frame_number / fps

        rows.append(
            {
                "frame": result.frame_number,
                "time_seconds": time_seconds,
                "frame_change_score": result.frame_change_score,
                "brightness_change": result.brightness_change,
                "brightness_normalized_change": (
                    result.brightness_normalized_change
                ),
            }
        )

    dataframe = pd.DataFrame(rows)
    dataframe.to_csv(output, index=False)

def save_frame_difference_images(
    previous_frame: NDArray[np.uint8],
    current_frame: NDArray[np.uint8],
    output_directory: str,
    prefix: str,
) -> None:
    """Save the previous, current, and difference images."""

    output_dir = Path(output_directory)
    output_dir.mkdir(parents=True, exist_ok=True)

    previous_gray = cv2.cvtColor(previous_frame, cv2.COLOR_BGR2GRAY)
    current_gray = cv2.cvtColor(current_frame, cv2.COLOR_BGR2GRAY)

    difference = cv2.absdiff(previous_gray, current_gray)

    previous_output = output_dir / f"{prefix}_previous.jpg"
    current_output = output_dir / f"{prefix}_current.jpg"
    difference_output = output_dir / f"{prefix}_difference.jpg"

    cv2.imwrite(str(previous_output), previous_frame)
    cv2.imwrite(str(current_output), current_frame)
    cv2.imwrite(str(difference_output), difference)

def calculate_brightness_change(
    previous_frame: NDArray[np.uint8],
    current_frame: NDArray[np.uint8],
) -> float:
    """Calculate the change in average brightness between two frames."""

    previous_gray = cv2.cvtColor(previous_frame, cv2.COLOR_BGR2GRAY)
    current_gray = cv2.cvtColor(current_frame, cv2.COLOR_BGR2GRAY)

    previous_brightness = float(np.mean(previous_gray))
    current_brightness = float(np.mean(current_gray))

    brightness_change = abs(current_brightness - previous_brightness)

    return brightness_change    

def calculate_brightness_normalized_difference(
    previous_frame: NDArray[np.uint8],
    current_frame: NDArray[np.uint8],
) -> float:
    """Calculate frame difference after removing average brightness."""

    previous_gray = cv2.cvtColor(previous_frame, cv2.COLOR_BGR2GRAY)
    current_gray = cv2.cvtColor(current_frame, cv2.COLOR_BGR2GRAY)

    previous_float = previous_gray.astype(np.float32)
    current_float = current_gray.astype(np.float32)

    previous_normalized = previous_float - np.mean(previous_float)
    current_normalized = current_float - np.mean(current_float)

    difference = np.abs(
        current_normalized - previous_normalized
    )

    return float(np.mean(difference))