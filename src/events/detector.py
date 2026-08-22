from dataclasses import dataclass
from pathlib import Path

import numpy as np
import pandas as pd


@dataclass
class DetectedEvent:
    """Store information about one detected event."""

    start_frame: int
    end_frame: int
    peak_frame: int
    peak_score: float

@dataclass
class EventCandidate:
    """Store one candidate frame for event detection."""

    frame_number: int
    score: float


def calculate_event_threshold(
    scores: list[float],
    percentile: float = 95.0,
) -> float:
    """Calculate an event detection threshold using a percentile."""

    threshold = float(
        np.percentile(scores, percentile)
    )

    return threshold

def find_event_candidates(
    analysis_results,
    threshold: float,
) -> list[EventCandidate]:
    """Find frame analysis results above the event threshold."""

    candidates = []

    for result in analysis_results:
        if result.brightness_normalized_change >= threshold:
            candidates.append(
                EventCandidate(
                    frame_number=result.frame_number,
                    score=result.brightness_normalized_change,
                )
            )

    return candidates

def group_event_candidates(
    candidates: list[EventCandidate],
    max_gap: int = 2,
) -> list[list[EventCandidate]]:
    """Group nearby event candidates into events."""

    if not candidates:
        return []

    groups = []
    current_group = [candidates[0]]

    for candidate in candidates[1:]:
        previous_candidate = current_group[-1]

        if (
            candidate.frame_number
            - previous_candidate.frame_number
            <= max_gap
        ):
            current_group.append(candidate)
        else:
            groups.append(current_group)
            current_group = [candidate]

    groups.append(current_group)

    return groups

def build_detected_events(
    event_groups: list[list[EventCandidate]],
) -> list[DetectedEvent]:
    """Convert grouped event candidates into detected events."""

    detected_events = []

    for group in event_groups:
        start_frame = group[0].frame_number
        end_frame = group[-1].frame_number

        peak_candidate = max(
            group,
            key=lambda candidate: candidate.score,
        )

        peak_frame = peak_candidate.frame_number
        peak_score = peak_candidate.score

        detected_events.append(
            DetectedEvent(
                start_frame=start_frame,
                end_frame=end_frame,
                peak_frame=peak_frame,
                peak_score=peak_score,
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

        rows.append(
            {
                "event_id": event_id,
                "start_frame": event.start_frame,
                "end_frame": event.end_frame,
                "start_time": event.start_frame / fps,
                "end_time": event.end_frame / fps,
                "peak_frame": event.peak_frame,
                "peak_time": event.peak_frame / fps,
                "peak_score": event.peak_score,
            }
        )

    dataframe = pd.DataFrame(rows)
    dataframe.to_csv(output, index=False)