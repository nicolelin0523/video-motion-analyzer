from dataclasses import dataclass
from pathlib import Path

import numpy as np
import pandas as pd


@dataclass
class ShotAnalysis:
    """Store analysis results for one shot."""

    shot_id: int
    start_frame: int
    end_frame: int
    duration_seconds: float
    average_motion_score: float
    maximum_motion_score: float
    event_count: int
    motion_level: str

def get_shot_analysis_results(
    shot,
    analysis_results,
):
    """Get frame analysis results that belong to one shot."""

    shot_results = [
        result
        for result in analysis_results
        if shot.start_frame + 1 < result.frame_number <= shot.end_frame + 1
    ]

    return shot_results

def analyze_shot(
    shot,
    analysis_results,
    events,
    fps: float,
) -> ShotAnalysis:
    """Analyze one shot and return its summary."""

    shot_results = get_shot_analysis_results(
        shot,
        analysis_results,
    )

    # 如果 shot 太短，沒有可分析的相鄰 frame pair
    if not shot_results:
        return ShotAnalysis(
            shot_id=shot.shot_id,
            start_frame=shot.start_frame,
            end_frame=shot.end_frame,
            duration_seconds=(
                shot.end_frame - shot.start_frame + 1
            ) / fps,
            average_motion_score=0.0,
            maximum_motion_score=0.0,
            event_count=0,
            motion_level="N/A",
        )

    normalized_scores = [
        result.brightness_normalized_change
        for result in shot_results
    ]

    average_motion_score = float(np.mean(normalized_scores))
    maximum_motion_score = float(np.max(normalized_scores))

    event_count = sum(
        1
        for event in events
        if shot.start_frame + 1 <= event.peak_frame <= shot.end_frame + 1
    )

    duration_seconds = (
        shot.end_frame - shot.start_frame + 1
    ) / fps

    return ShotAnalysis(
        shot_id=shot.shot_id,
        start_frame=shot.start_frame,
        end_frame=shot.end_frame,
        duration_seconds=duration_seconds,
        average_motion_score=average_motion_score,
        maximum_motion_score=maximum_motion_score,
        event_count=event_count,
        motion_level="Unclassified",
    )

def analyze_all_shots(
    shots,
    analysis_results,
    events,
    fps: float,
) -> list[ShotAnalysis]:
    """Analyze all shots in the video."""

    shot_analyses = []

    for shot in shots:
        shot_analysis = analyze_shot(
            shot=shot,
            analysis_results=analysis_results,
            events=events,
            fps=fps,
        )

        shot_analyses.append(shot_analysis)

    assign_motion_levels(shot_analyses)

    return shot_analyses

def save_shot_analyses_to_csv(
    shot_analyses: list[ShotAnalysis],
    output_path: str,
) -> None:
    """Save shot-level analysis results to a CSV file."""

    output = Path(output_path)
    output.parent.mkdir(parents=True, exist_ok=True)

    rows = []

    for shot_analysis in shot_analyses:
        rows.append(
            {
                "shot_id": shot_analysis.shot_id,
                "start_frame": shot_analysis.start_frame,
                "end_frame": shot_analysis.end_frame,
                "duration_seconds": shot_analysis.duration_seconds,
                "average_motion_score": shot_analysis.average_motion_score,
                "maximum_motion_score": shot_analysis.maximum_motion_score,
                "event_count": shot_analysis.event_count,
                "motion_level": shot_analysis.motion_level, 
            }
        )

    dataframe = pd.DataFrame(rows)
    dataframe.to_csv(output, index=False)

def assign_motion_levels(
    shot_analyses: list[ShotAnalysis],
) -> None:
    """Assign Low, Medium, or High motion levels to shots."""

    valid_scores = [
        shot_analysis.average_motion_score
        for shot_analysis in shot_analyses
        if shot_analysis.motion_level != "N/A"
    ]

    low_threshold = float(np.percentile(valid_scores, 33))
    high_threshold = float(np.percentile(valid_scores, 66))

    for shot_analysis in shot_analyses:
        if shot_analysis.motion_level == "N/A":
            continue

        if shot_analysis.average_motion_score <= low_threshold:
            shot_analysis.motion_level = "Low"

        elif shot_analysis.average_motion_score <= high_threshold:
            shot_analysis.motion_level = "Medium"

        else:
            shot_analysis.motion_level = "High"