from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np


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