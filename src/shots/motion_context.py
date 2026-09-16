import csv
from dataclasses import dataclass
from pathlib import Path

from src.motion.optical_flow import (
    calculate_mean_adjacent_change,
    calculate_shot_motion_magnitude,
    calculate_shot_motion_std,
)


@dataclass
class ShotMotionContext:
    shot_id: int
    start_frame: int
    end_frame: int
    num_pairs: int
    motion_magnitude: float
    motion_std: float
    mean_adjacent_change: float

def build_shot_motion_context(
    shot_id: int,
    start_frame: int,
    end_frame: int,
    magnitudes: list[float],
) -> ShotMotionContext:
    if not magnitudes:
        raise ValueError("Magnitudes cannot be empty.")

    return ShotMotionContext(
        shot_id=shot_id,
        start_frame=start_frame,
        end_frame=end_frame,
        num_pairs=len(magnitudes),
        motion_magnitude=calculate_shot_motion_magnitude(magnitudes),
        motion_std=calculate_shot_motion_std(magnitudes),
        mean_adjacent_change=calculate_mean_adjacent_change(magnitudes),
    )

def save_shot_motion_contexts_to_csv(
    contexts: list[ShotMotionContext],
    output_path: Path,
) -> None:
    output_path.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    with output_path.open(
        "w",
        newline="",
        encoding="utf-8",
    ) as csv_file:
        writer = csv.writer(csv_file)

        writer.writerow(
            [
                "shot_id",
                "start_frame",
                "end_frame",
                "num_pairs",
                "motion_magnitude",
                "motion_std",
                "mean_adjacent_change",
            ]
        )

        for context in contexts:
            writer.writerow(
                [
                    context.shot_id,
                    context.start_frame,
                    context.end_frame,
                    context.num_pairs,
                    context.motion_magnitude,
                    context.motion_std,
                    context.mean_adjacent_change,
                ]
            )