import argparse

import numpy as np

from src.motion.frame_difference import save_motion_scores_to_csv
from src.video.reader import (
    calculate_video_motion_scores,
    count_readable_frames,
    read_video_metadata,
)


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
        motion_scores = calculate_video_motion_scores(video_path)
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

    output_path = "outputs/motion_scores.csv"

    save_motion_scores_to_csv(
        motion_scores=motion_scores,
        fps=metadata.fps,
        output_path=output_path,
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
    print(f"Motion scores saved to: {output_path}")


if __name__ == "__main__":
    main()