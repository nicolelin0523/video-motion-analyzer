def print_analysis_summary(
    metadata,
    average_score: float,
    maximum_score: float,
    maximum_score_time: float,
    maximum_normalized_score: float,
    maximum_normalized_time: float,
    maximum_difference_score: float,
    maximum_difference_time: float,
    csv_output_path: str,
    events_output_path: str,
    plot_output_path: str,
) -> None:
    """Print a summary of the video analysis results."""

    print("Video Motion Analyzer")
    print("---------------------")
    print(f"Video path: {metadata.path}")
    print(f"Resolution: {metadata.width} x {metadata.height}")
    print(f"FPS: {metadata.fps:.2f}")
    print(f"Duration: {metadata.duration_seconds:.2f} seconds")

    print()
    print("Analysis Summary")
    print("----------------")
    print(f"Average frame change score: {average_score:.2f}")
    print(
        f"Maximum frame change: "
        f"{maximum_score:.2f} at {maximum_score_time:.2f}s"
    )
    print(
        f"Maximum brightness-normalized change: "
        f"{maximum_normalized_score:.2f} at "
        f"{maximum_normalized_time:.2f}s"
    )
    print(
        f"Largest normalization difference: "
        f"{maximum_difference_score:.2f} at "
        f"{maximum_difference_time:.2f}s"
    )

    print()
    print("Outputs")
    print("-------")
    print(f"CSV saved to: {csv_output_path}")
    print(f"Events CSV saved to: {events_output_path}")
    print(f"Motion curve saved to: {plot_output_path}")
    print("Frame images saved to: outputs")