import argparse

import numpy as np

from src.motion.frame_difference import (
    save_analysis_results_to_csv,
    save_frame_difference_images,
)
from src.video.reader import (
    analyze_video_frames,
    count_readable_frames,
    read_frame_pair,
    read_video_metadata,
)
from src.visualization.plotter import plot_motion_curve


def parse_arguments() -> argparse.Namespace:
    """Parse command-line arguments."""

    parser = argparse.ArgumentParser(
        description="Analyze basic metadata from a video file."
    )

    parser.add_argument(
        "--video",
        required=True,
        help="Path to the input video file.",
    )

    return parser.parse_args()


def main() -> None:
    """Run the Video Motion Analyzer application."""

    args = parse_arguments()
    video_path = args.video

    try:
        metadata = read_video_metadata(video_path)
        readable_frame_count = count_readable_frames(video_path)
        analysis_results = analyze_video_frames(video_path)
        motion_scores = [
            result.frame_change_score
            for result in analysis_results
        ]
    except FileNotFoundError as error:
        print(f"Error: {error}")
        return
    except ValueError as error:
        print(f"Error: {error}")
        return
    average_score = float(np.mean(motion_scores))
    minimum_score = float(np.min(motion_scores))
    maximum_score = float(np.max(motion_scores))

    maximum_score_index = int(np.argmax(motion_scores))
    maximum_score_frame = maximum_score_index + 2
    maximum_score_time = maximum_score_frame / metadata.fps
    normalized_scores = [
        result.brightness_normalized_change
        for result in analysis_results
    ]

    maximum_normalized_index = int(np.argmax(normalized_scores))

    maximum_normalized_result = analysis_results[
        maximum_normalized_index
    ]
    
    normalized_previous_frame, normalized_current_frame = read_frame_pair(
        video_path=video_path,
        current_frame_number=maximum_normalized_result.frame_number,
    )

    save_frame_difference_images(
        previous_frame=normalized_previous_frame,
        current_frame=normalized_current_frame,
        output_directory="outputs",
        prefix="max_normalized_change",
    )

    previous_frame, current_frame = read_frame_pair(
        video_path=video_path,
        current_frame_number=maximum_score_frame,
    )
    save_frame_difference_images(
        previous_frame=previous_frame,
        current_frame=current_frame,
        output_directory="outputs",
        prefix="max_change",
    )

    
    csv_output_path = "outputs/motion_scores.csv"
    plot_output_path = "outputs/motion_curve.png"

    save_analysis_results_to_csv(
        analysis_results=analysis_results,
        fps=metadata.fps,
        output_path=csv_output_path,
    )
    plot_motion_curve(
        motion_scores=motion_scores,
        fps=metadata.fps,
        output_path=plot_output_path,
    )

    print("Video Motion Analyzer")
    print("---------------------")
    print(f"Video path: {metadata.path}")
    print(f"Resolution: {metadata.width} x {metadata.height}")
    print(f"FPS: {metadata.fps:.2f}")
    print(f"Metadata frame count: {metadata.frame_count}")
    print(f"Readable frame count: {readable_frame_count}")
    print(f"Duration: {metadata.duration_seconds:.2f} seconds")
    print(f"Motion score count: {len(motion_scores)}")
    print(f"Average frame change score: {average_score:.2f}")
    print(f"Minimum frame change score: {minimum_score:.2f}")
    print(f"Maximum frame change score: {maximum_score:.2f}")
    print(f"Maximum change occurs at frame: {maximum_score_frame}")
    print(f"Maximum change time: {maximum_score_time:.2f} seconds")
    print(f"Motion scores saved to: {csv_output_path}")
    print(f"Motion curve saved to: {plot_output_path}")
    print("Maximum change frame images saved to: outputs")
    print(
        "Maximum brightness-normalized change: "
        f"{maximum_normalized_result.brightness_normalized_change:.2f}"
    )
    print(
        "Maximum normalized change frame: "
        f"{maximum_normalized_result.frame_number}"
    )
    print(
        "Maximum normalized change time: "
        f"{maximum_normalized_result.frame_number / metadata.fps:.2f}s"
    )
    print("Maximum normalized change frame images saved to: outputs")


if __name__ == "__main__":
    main()