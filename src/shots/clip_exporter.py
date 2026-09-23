from pathlib import Path

import cv2


def export_shot_clip(
    video_path: Path,
    start_frame: int,
    end_frame: int,
    output_path: Path,
) -> None:
    cap = cv2.VideoCapture(str(video_path))

    if not cap.isOpened():
        raise ValueError(f"Cannot open video: {video_path}")

    fps = cap.get(cv2.CAP_PROP_FPS)
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

    output_path.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    fourcc = cv2.VideoWriter_fourcc(*"mp4v")

    writer = cv2.VideoWriter(
        str(output_path),
        fourcc,
        fps,
        (width, height),
    )

    if not writer.isOpened():
        cap.release()
        raise ValueError(f"Cannot create output video: {output_path}")

    cap.set(
        cv2.CAP_PROP_POS_FRAMES,
        start_frame,
    )

    for _ in range(start_frame, end_frame + 1):
        ret, frame = cap.read()

        if not ret:
            break

        writer.write(frame)

    writer.release()
    cap.release()