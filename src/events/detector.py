from dataclasses import dataclass
from pathlib import Path

import numpy as np
import pandas as pd


@dataclass
class DetectedEvent:
    """Store information about one detected event."""

    start_index: int
    end_index: int
    peak_index: int
    peak_score: float
    event_type: str


def calculate_event_threshold(
    scores: list[float],
    percentile: float = 95.0,
) -> float:
    """Calculate an event detection threshold using a percentile."""

    threshold = float(
        np.percentile(scores, percentile)
    )

    return threshold

def find_candidate_event_indices(
    scores: list[float],
    threshold: float,
) -> list[int]:
    """Find indices whose scores are above the event threshold."""

    candidate_indices = []

    for index, score in enumerate(scores):
        if score >= threshold:
            candidate_indices.append(index)

    return candidate_indices

def group_candidate_indices(
    candidate_indices: list[int],
    max_gap: int = 2,
) -> list[list[int]]:
    """Group consecutive candidate indices into events."""

    if not candidate_indices:
        return []

    groups = []
    current_group = [candidate_indices[0]]

    for index in candidate_indices[1:]:
        if index - current_group[-1] <= max_gap:
            current_group.append(index)
        else:
            groups.append(current_group)
            current_group = [index]

    groups.append(current_group)

    return groups

def build_detected_events(
    event_groups: list[list[int]],
    scores: list[float],
    cut_threshold: float,
) -> list[DetectedEvent]:
    """Convert grouped candidate indices into detected events."""

    detected_events = []

    for group in event_groups:
        start_index = group[0]
        end_index = group[-1]

        peak_index = max(
            group,
            key=lambda index: scores[index],
        )

        peak_score = scores[peak_index]

        if peak_score >= cut_threshold:
            event_type = "possible_cut"
        else:
            event_type = "motion_candidate"

        detected_events.append(
            DetectedEvent(
                start_index=start_index,
                end_index=end_index,
                peak_index=peak_index,
                peak_score=peak_score,
                event_type=event_type,
            )
        )

    return detected_events

def save_events_to_csv(
    detected_events: list[DetectedEvent],
    fps: float,
    output_path: str,
) -> None:
    """Save detected events to a CSV file."""

    output = Path(output_path)
    output.parent.mkdir(parents=True, exist_ok=True)

    rows = []

    for event_id, event in enumerate(
        detected_events,
        start=1,
    ):
        start_frame = event.start_index + 2
        end_frame = event.end_index + 2
        peak_frame = event.peak_index + 2

        rows.append(
            {
                "event_id": event_id,
                "start_frame": start_frame,
                "end_frame": end_frame,
                "start_time": start_frame / fps,
                "end_time": end_frame / fps,
                "peak_frame": peak_frame,
                "peak_time": peak_frame / fps,
                "peak_score": event.peak_score,
                "event_type": event.event_type,
            }
        )

    dataframe = pd.DataFrame(rows)
    dataframe.to_csv(output, index=False)