from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import Patch


def plot_motion_curve(
    motion_scores: list[float],
    fps: float,
    output_path: str,
) -> None:
    """Plot frame change scores over video time and save the figure."""

    output = Path(output_path)
    output.parent.mkdir(parents=True, exist_ok=True)

    time_seconds = [
        (index + 2) / fps
        for index in range(len(motion_scores))
    ]

    maximum_index = int(np.argmax(motion_scores))
    maximum_time = time_seconds[maximum_index]
    maximum_score = motion_scores[maximum_index]

    plt.figure(figsize=(12, 5))
    plt.plot(time_seconds, motion_scores)

    plt.scatter(
        maximum_time,
        maximum_score,
        zorder=3,
    )

    plt.annotate(
        f"Max: {maximum_score:.2f}\nTime: {maximum_time:.2f}s",
        xy=(maximum_time, maximum_score),
        xytext=(maximum_time + 5, maximum_score - 10),
        arrowprops={"arrowstyle": "->"},
    )

    plt.title("Video Frame Change Curve")
    plt.xlabel("Time (seconds)")
    plt.ylabel("Average Pixel Difference")
    plt.grid(True, alpha=0.3)
    plt.tight_layout()

    plt.savefig(output, dpi=150)
    plt.close()

def plot_comparison_curve(
    motion_scores: list[float],
    normalized_scores: list[float],
    fps: float,
    output_path: str,
    highlight_index: int,
    normalized_highlight_index: int,
) -> None:
    """Plot original and brightness-normalized frame change curves."""

    output = Path(output_path)
    output.parent.mkdir(parents=True, exist_ok=True)

    time_seconds = [
        (index + 2) / fps
        for index in range(len(motion_scores))
    ]
    highlight_time = time_seconds[highlight_index]
    highlight_score = motion_scores[highlight_index]
    normalized_highlight_time = time_seconds[
        normalized_highlight_index
    ]

    normalized_highlight_score = normalized_scores[
        normalized_highlight_index
    ]

    plt.figure(figsize=(12, 5))

    plt.plot(
        time_seconds,
        motion_scores,
        label="Original Frame Change",
    )

    plt.plot(
        time_seconds,
        normalized_scores,
        label="Brightness-Normalized Change",
    )

    plt.scatter(
        highlight_time,
        highlight_score,
        zorder=3,
    )

    plt.annotate(
        "Largest normalization difference",
        xy=(highlight_time, highlight_score),
        xytext=(highlight_time + 5, highlight_score - 15),
        arrowprops={"arrowstyle": "->"},
    )

    plt.scatter(
        normalized_highlight_time,
        normalized_highlight_score,
        zorder=3,
    )

    plt.annotate(
        "Maximum normalized change",
        xy=(
            normalized_highlight_time,
            normalized_highlight_score,
        ),
        xytext=(
            normalized_highlight_time + 5,
            normalized_highlight_score - 15,
        ),
        arrowprops={"arrowstyle": "->"},
    )

    plt.title("Frame Change Comparison")
    plt.xlabel("Time (seconds)")
    plt.ylabel("Change Score")

    plt.legend()
    plt.grid(True, alpha=0.3)
    plt.tight_layout()

    plt.savefig(output, dpi=150)
    plt.close()

def plot_shot_motion_scores(
    shot_analyses,
    output_path: str,
) -> None:
    """Plot average motion score for each shot."""

    shot_ids = [
        shot_analysis.shot_id
        for shot_analysis in shot_analyses
    ]

    average_scores = [
        shot_analysis.average_motion_score
        for shot_analysis in shot_analyses
    ]

    motion_levels = [
        shot_analysis.motion_level
        for shot_analysis in shot_analyses
    ]

    level_to_color = {
        "Low": "tab:blue",
        "Medium": "tab:orange",
        "High": "tab:red",
        "N/A": "tab:gray",
    }

    bar_colors = [
        level_to_color[level]
        for level in motion_levels
    ]

    plt.figure(figsize=(12, 6))

    plt.bar(
        shot_ids,
        average_scores,
        color=bar_colors,
    )

    plt.xlabel("Shot ID")
    plt.ylabel("Average Motion Score")
    plt.title("Average Motion Score by Shot")

    legend_handles = [
        Patch(color="tab:blue", label="Low"),
        Patch(color="tab:orange", label="Medium"),
        Patch(color="tab:red", label="High"),
        Patch(color="tab:gray", label="N/A"),
    ]
    plt.legend(handles=legend_handles)

    plt.tight_layout()
    plt.savefig(output_path)
    plt.close()

def plot_shot_motion_and_events(
    shot_analyses,
    output_path: str,
) -> None:
    """Plot average motion score and event rate for each shot."""

    shot_ids = [
        shot_analysis.shot_id
        for shot_analysis in shot_analyses
    ]

    average_scores = [
        shot_analysis.average_motion_score
        for shot_analysis in shot_analyses
    ]

    event_rates = [
        shot_analysis.event_rate
        for shot_analysis in shot_analyses
    ]

    figure, left_axis = plt.subplots(figsize=(12, 6))

    left_axis.bar(
        shot_ids,
        average_scores,
        alpha=0.7,
        label="Average Motion Score",
    )

    left_axis.set_xlabel("Shot ID")
    left_axis.set_ylabel("Average Motion Score")

    right_axis = left_axis.twinx()

    right_axis.plot(
        shot_ids,
        event_rates,
        marker="o",
        label="Event Rate",
    )

    right_axis.set_ylabel("Event Rate (events/second)")

    plt.title("Shot Motion Score and Event Rate")

    figure.tight_layout()
    figure.savefig(output_path)
    plt.close(figure)

def plot_shot_event_rates(
    shot_analyses,
    output_path: str,
) -> None:
    """Plot event rate for each shot."""

    shot_ids = [
        shot_analysis.shot_id
        for shot_analysis in shot_analyses
    ]

    event_rates = [
        shot_analysis.event_rate
        for shot_analysis in shot_analyses
    ]

    plt.figure(figsize=(12, 6))

    plt.bar(
        shot_ids,
        event_rates,
    )

    plt.xlabel("Shot ID")
    plt.ylabel("Event Rate (events/second)")
    plt.title("Event Rate by Shot")

    plt.tight_layout()
    plt.savefig(output_path)
    plt.close()

def plot_shot_motion_magnitude(
    contexts,
    output_path,
) -> None:
    shot_ids = [
        context.shot_id
        for context in contexts
    ]

    motion_magnitudes = [
        context.motion_magnitude
        for context in contexts
    ]

    plt.figure(figsize=(12, 6))

    plt.plot(
        shot_ids,
        motion_magnitudes,
        marker="o",
    )

    plt.xlabel("Shot ID")
    plt.ylabel("Motion Magnitude")
    plt.title("Shot-level Motion Magnitude")

    plt.grid(True)
    plt.tight_layout()

    plt.savefig(output_path)
    plt.close()

def plot_shot_motion_stability(
    contexts,
    output_path,
) -> None:
    shot_ids = [
        context.shot_id
        for context in contexts
    ]

    adjacent_changes = [
        context.mean_adjacent_change
        for context in contexts
    ]

    plt.figure(figsize=(12, 6))

    plt.plot(
        shot_ids,
        adjacent_changes,
        marker="o",
    )

    plt.xlabel("Shot ID")
    plt.ylabel("Mean Adjacent Change")
    plt.title("Shot-level Motion Stability")

    plt.grid(True)
    plt.tight_layout()

    plt.savefig(output_path)
    plt.close()