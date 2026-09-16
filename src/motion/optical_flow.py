import cv2
import numpy as np


def calculate_optical_flow_magnitude(
    previous_frame: np.ndarray,
    current_frame: np.ndarray,
) -> float:
    previous_gray = cv2.cvtColor(previous_frame, cv2.COLOR_BGR2GRAY)
    current_gray = cv2.cvtColor(current_frame, cv2.COLOR_BGR2GRAY)

    flow = cv2.calcOpticalFlowFarneback(
        previous_gray,
        current_gray,
        None,
        0.5,
        3,
        15,
        3,
        5,
        1.2,
        0,
    )
    magnitude, _ = cv2.cartToPolar(
        flow[..., 0],
        flow[..., 1],
    )
    mean_magnitude = np.mean(magnitude)
    return float(mean_magnitude)

def calculate_shot_motion_magnitudes(
    video_path,
    start_frame,
    end_frame,
):
    cap = cv2.VideoCapture(str(video_path))
    cap.set(cv2.CAP_PROP_POS_FRAMES, start_frame)
    ret, previous_frame = cap.read()

    if not ret:
        cap.release()
        raise ValueError(
            f"Cannot read start frame: {start_frame}"
        )
    magnitudes = []
    for _ in range(start_frame + 1, end_frame + 1):
        ret, current_frame = cap.read()

        if not ret:
            break

        magnitude = calculate_optical_flow_magnitude(
            previous_frame,
            current_frame,
        )

        magnitudes.append(magnitude)

        previous_frame = current_frame

    cap.release()

    return magnitudes

def calculate_shot_motion_magnitude(
    magnitudes: list[float],
) -> float:
    if not magnitudes:
        raise ValueError("Magnitudes cannot be empty.")

    return float(np.median(magnitudes))

def calculate_shot_motion_std(
    magnitudes: list[float],
) -> float:
    if not magnitudes:
        raise ValueError("Magnitudes cannot be empty.")

    return float(np.std(magnitudes))

def calculate_mean_adjacent_change(
    magnitudes: list[float],
) -> float:
    if len(magnitudes) < 2:
        return 0.0

    changes = np.abs(np.diff(magnitudes))

    return float(np.mean(changes))