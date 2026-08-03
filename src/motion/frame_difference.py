from pathlib import Path

import cv2
import numpy as np
import pandas as pd
from numpy.typing import NDArray


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

def save_motion_scores_to_csv(
    motion_scores: list[float],
    fps: float,
    output_path: str,
) -> None:
    """Save frame change scores and timestamps to a CSV file."""

    output = Path(output_path)
    output.parent.mkdir(parents=True, exist_ok=True)

    rows = []

    for index, score in enumerate(motion_scores):
        frame_number = index + 2
        time_seconds = frame_number / fps

        rows.append(
            {
                "frame": frame_number,
                "time_seconds": time_seconds,
                "frame_change_score": score,
            }
        )

    dataframe = pd.DataFrame(rows)
    dataframe.to_csv(output, index=False)