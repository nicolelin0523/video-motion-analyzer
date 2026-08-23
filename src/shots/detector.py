from dataclasses import dataclass

from scenedetect import ContentDetector, detect


@dataclass
class Shot:
    """Store the frame range of one detected shot."""

    shot_id: int
    start_frame: int
    end_frame: int

def detect_shots(
    video_path: str,
) -> list[Shot]:
    """Detect shots in a video using PySceneDetect."""

    scene_list = detect(
        video_path,
        ContentDetector(),
    )

    shots = []

    for shot_id, (start_time, end_time) in enumerate(
        scene_list,
        start=1,
    ):
        start_frame = start_time.get_frames()
        end_frame = end_time.get_frames() - 1

        shots.append(
            Shot(
                shot_id=shot_id,
                start_frame=start_frame,
                end_frame=end_frame,
            )
        )

    return shots

def get_boundary_frame_numbers(
    shots: list[Shot],
) -> set[int]:
    """Get frame numbers whose frame pairs cross shot boundaries."""

    boundary_frame_numbers = set()

    for shot in shots[1:]:
        boundary_frame_number = shot.start_frame + 1
        boundary_frame_numbers.add(boundary_frame_number)

    return boundary_frame_numbers

def filter_shot_boundary_results(
    analysis_results,
    shots: list[Shot],
):
    """Remove frame analysis results that cross shot boundaries."""

    boundary_frame_numbers = get_boundary_frame_numbers(
        shots
    )

    within_shot_results = [
        result
        for result in analysis_results
        if result.frame_number not in boundary_frame_numbers
    ]

    return within_shot_results