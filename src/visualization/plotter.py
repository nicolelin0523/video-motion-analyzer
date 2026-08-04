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