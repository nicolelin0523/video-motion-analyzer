import argparse

from src.video.reader import read_video_metadata


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
    except FileNotFoundError as error:
        print(f"Error: {error}")
        return
    except ValueError as error:
        print(f"Error: {error}")
        return

    print("Video Motion Analyzer")
    print("---------------------")
    print(f"Video path: {metadata.path}")
    print(f"Resolution: {metadata.width} x {metadata.height}")
    print(f"FPS: {metadata.fps:.2f}")
    print(f"Frame count: {metadata.frame_count}")
    print(f"Duration: {metadata.duration_seconds:.2f} seconds")


if __name__ == "__main__":
    main()