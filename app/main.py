import argparse

import numpy as np

from src.events.detector import (
    detect_events,
    save_events_to_csv,
)
from src.motion.frame_difference import (
    save_analysis_results_to_csv,
    save_frame_difference_images,
)
from src.output.reporter import print_analysis_summary
from src.shots.detector import (
    detect_shots,
    filter_shot_boundary_results,
)
from src.video.reader import (
    analyze_video_frames,
    read_frame_pair,
    read_video_metadata,
)
from src.visualization.plotter import (
    plot_comparison_curve,
    plot_motion_curve,
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
        # 讀取影片基本資訊，並計算每組相鄰 frame 的變化
        metadata = read_video_metadata(video_path)
        analysis_results = analyze_video_frames(video_path)

        # 偵測 shot，並排除跨 shot 的 frame pair
        shots = detect_shots(video_path)
        within_shot_results = filter_shot_boundary_results(
            analysis_results,
            shots,
        )
        # 取出原始 frame change score，供後續統計與畫圖使用
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

    # 計算原始 frame change 的平均值與最大值
    average_score = float(np.mean(motion_scores))
    maximum_score = float(np.max(motion_scores))

    maximum_score_index = int(np.argmax(motion_scores))
    maximum_score_frame = maximum_score_index + 2
    maximum_score_time = maximum_score_frame / metadata.fps

    # 取出亮度正規化後的 frame change score
    normalized_scores = [
        result.brightness_normalized_change
        for result in analysis_results
    ]

    # 只使用 shot 內的資料偵測高變化事件
    events = detect_events(
        within_shot_results
    )

    events_output_path = "outputs/events.csv"

    save_events_to_csv(
        events=events,
        fps=metadata.fps,
        output_path=events_output_path,
    )

    # 比較原始 score 與正規化 score，
    # 找出受亮度影響最明顯的位置
    score_differences = [
        original - normalized
        for original, normalized in zip(
            motion_scores,
            normalized_scores,
        )
    ]

    maximum_difference_index = int(np.argmax(score_differences))
    maximum_difference_result = analysis_results[
        maximum_difference_index
    ]
    maximum_difference_score = score_differences[
        maximum_difference_index
    ]

    # 找出亮度正規化後變化最大的 frame pair
    maximum_normalized_index = int(np.argmax(normalized_scores))
    maximum_normalized_result = analysis_results[
        maximum_normalized_index
    ]

    # 儲存「正規化後變化最大」的前後 frame 與差分圖
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

    # 儲存「原始 frame change 最大」的前後 frame 與差分圖
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

    # 儲存完整 frame analysis 結果
    csv_output_path = "outputs/motion_scores.csv"
    plot_output_path = "outputs/motion_curve.png"

    save_analysis_results_to_csv(
        analysis_results=analysis_results,
        fps=metadata.fps,
        output_path=csv_output_path,
    )
    # 畫出原始 frame change 曲線
    plot_motion_curve(
        motion_scores=motion_scores,
        fps=metadata.fps,
        output_path=plot_output_path,
    )

    # 畫出原始 score 與 brightness-normalized score 的比較圖
    comparison_output_path = "outputs/comparison_curve.png"

    plot_comparison_curve(
        motion_scores=motion_scores,
        normalized_scores=normalized_scores,
        fps=metadata.fps,
        output_path=comparison_output_path,
        highlight_index=maximum_difference_index,
        normalized_highlight_index=maximum_normalized_index,
    )

    # 在終端機顯示分析摘要
    print_analysis_summary(
        metadata=metadata,
        average_score=average_score,
        maximum_score=maximum_score,
        maximum_score_time=maximum_score_time,
        maximum_normalized_score=(
            maximum_normalized_result.brightness_normalized_change
        ),
        maximum_normalized_time=(
            maximum_normalized_result.frame_number / metadata.fps
        ),
        maximum_difference_score=maximum_difference_score,
        maximum_difference_time=(
            maximum_difference_result.frame_number / metadata.fps
        ),
        csv_output_path=csv_output_path,
        events_output_path=events_output_path,
        plot_output_path=plot_output_path,
    )

if __name__ == "__main__":
    main()