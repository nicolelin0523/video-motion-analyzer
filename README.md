# Video Motion Analyzer

A Python-based video analysis project for extracting and analyzing motion-related information from videos.

This project combines **frame-level visual change analysis**, **shot detection**, and **optical-flow-based motion analysis** to build a structured video processing pipeline.

The current focus is on analyzing motion characteristics within individual shots and providing quantitative features that can be used for further video understanding and motion-aware processing.

---

## Project Overview

Video contains different types of motion across different shots.

Some shots may contain only small local movement, while others may include large object motion, camera movement, or rapid changes.

The goal of this project is to:

- Detect shot boundaries in a video
- Analyze frame-level visual changes
- Measure motion information using optical flow
- Build shot-level motion summaries
- Visualize and export motion analysis results
- Provide a modular pipeline for future motion-aware video processing

---

## Key Features

### 1. Video Information Extraction

The system reads basic video information, including:

- Resolution
- FPS
- Total number of frames
- Video duration

### 2. Frame Difference Analysis

Frame-to-frame visual changes are measured using pixel differences.

The system can calculate:

- Raw frame difference
- Normalized motion score
- Motion curve over time

This provides a simple way to observe where noticeable visual changes occur in the video.

### 3. Motion Event Detection

Motion events are detected based on a motion-score threshold.

The system can:

- Identify high-motion candidate frames
- Group neighboring candidates into motion events
- Rank motion events by motion intensity

This allows the user to quickly locate important motion segments within a video.

### 4. Shot Detection

The project uses **PySceneDetect** to divide a video into individual shots.

Each shot contains a continuous sequence of frames without a major scene transition.

Shot detection is useful because motion characteristics are often more consistent within the same shot than across different shots.

Detected shot information includes:

- Shot ID
- Start frame
- End frame
- Shot duration

### 5. Optical Flow Analysis

Optical flow is used to estimate motion between consecutive frames.

The current implementation uses **Farneback Optical Flow** from OpenCV.

For each pair of frames, the system calculates an optical flow magnitude representing the amount of motion between the two frames.

### 6. Shot-Level Motion Context

Instead of analyzing motion only at the frame level, the system summarizes motion information for each shot.

For every shot, the following features are calculated:

#### Motion Magnitude

Represents the overall motion intensity of the shot.

It is calculated from the average optical-flow magnitude across all consecutive frame pairs inside the shot.

#### Motion Stability — Standard Deviation

Measures how much the motion intensity varies within the shot.

A lower value indicates that motion remains relatively stable.

A higher value indicates larger motion variation.

#### Mean Adjacent Change

Measures the average difference in motion magnitude between consecutive frame pairs.

This feature describes how quickly the motion state changes over time.

---

## Example Motion Characteristics

Using the shot-level motion features, different types of shots can be observed.

### Low Motion + Stable

Example:

- Small local object movement
- Mostly static camera
- Low Motion Magnitude
- Low Mean Adjacent Change

### High Motion + Relatively Stable

Example:

- Continuous forward movement
- Consistent camera movement
- High Motion Magnitude
- Relatively low Mean Adjacent Change

### High Motion + Unstable

Example:

- Moving person combined with camera motion
- Rapid motion variation
- High Motion Magnitude
- High Mean Adjacent Change

These features allow motion characteristics to be quantitatively compared with the actual video content.

---

## Analysis Pipeline

```text
Input Video
    |
    v
Video Information Extraction
    |
    v
Frame Difference Analysis
    |
    v
Motion Event Detection
    |
    v
Shot Detection
    |
    v
Shot-Level Processing
    |
    +-----------------------------+
    |                             |
    v                             v
Frame-Level Analysis      Optical Flow Analysis
                                  |
                                  v
                       Shot Motion Magnitudes
                                  |
                                  v
                       Shot Motion Context
                                  |
                                  v
                    CSV / Plot / Video Outputs
```

---

## Project Structure

```text
video-motion-analyzer/
│
├── app/
│   └── main.py
│
├── src/
│   ├── motion/
│   │   └── optical_flow.py
│   │
│   ├── visualization/
│   │   └── plotter.py
│   │
│   └── ...
│
├── data/
│   └── sample.mp4
│
├── outputs/
│   ├── shot_motion_context.csv
│   ├── shot_motion_magnitude.png
│   ├── shot_motion_stability.png
│   └── shot_*.mp4
│
├── README.md
│
└── requirements.txt
```

> The project structure may continue to evolve as new modules are added.

---

## Core Modules

### Optical Flow

`src/motion/optical_flow.py`

Main functions include:

```python
calculate_optical_flow_magnitude(frame1, frame2)
```

Calculates the optical-flow magnitude between two frames.

```python
calculate_shot_motion_magnitudes(
    video_path,
    start_frame,
    end_frame,
)
```

Calculates optical-flow magnitudes for all consecutive frame pairs within a shot.

```python
build_shot_motion_context(
    shot_id,
    start_frame,
    end_frame,
    magnitudes,
)
```

Builds shot-level motion features.

```python
save_shot_motion_contexts_to_csv(...)
```

Exports shot-level motion analysis results to a CSV file.

Additional functions support:

- Motion magnitude visualization
- Motion stability visualization
- Shot clip exporting

---

## Output Files

The analysis results are stored in the `outputs/` directory.

### Shot Motion Context

```text
outputs/shot_motion_context.csv
```

Example columns:

| Column | Description |
| --- | --- |
| `shot_id` | Shot identifier |
| `start_frame` | First frame of the shot |
| `end_frame` | Last frame of the shot |
| `num_pairs` | Number of frame pairs |
| `motion_magnitude` | Average motion intensity |
| `motion_std` | Motion variation |
| `mean_adjacent_change` | Average change between consecutive motion values |

### Motion Magnitude Plot

```text
outputs/shot_motion_magnitude.png
```

Visualizes the overall motion intensity of different shots.

### Motion Stability Plot

```text
outputs/shot_motion_stability.png
```

Visualizes motion stability across shots.

### Shot Clips

```text
outputs/shot_<id>_<start>_<end>.mp4
```

Individual shot clips can be exported for visual comparison with the calculated motion features.

This allows quantitative results to be checked against the actual video content.

---

## Example Shot Analysis

Example shot-level motion analysis:

| Shot | Motion Magnitude | Motion STD | Mean Adjacent Change | Motion Characteristic |
| --- | ---: | ---: | ---: | --- |
| Shot 2 | 0.0036 | 0.0044 | 0.0022 | Low motion, stable |
| Shot 20 | 1.9601 | - | 0.1772 | High motion, relatively stable |
| Shot 24 | 5.6907 | - | 1.6612 | High motion, unstable |

Example interpretation:

- **Shot 2** contains only small local motion and remains relatively stable.
- **Shot 20** contains stronger motion but changes smoothly over time.
- **Shot 24** contains large and rapidly changing motion.

These examples demonstrate that the calculated motion features can describe different motion characteristics across video shots.

---

## Technologies

The project currently uses:

- Python
- OpenCV
- NumPy
- Pandas
- Matplotlib
- PySceneDetect
- Git
- GitHub

---

## Installation

Clone the repository:

```bash
git clone https://github.com/nicolelin0523/video-motion-analyzer.git
```

Move into the project directory:

```bash
cd video-motion-analyzer
```

Create a virtual environment:

```bash
python -m venv .venv
```

Activate the environment.

### Windows PowerShell

```powershell
.venv\Scripts\Activate.ps1
```

Install the required packages:

```bash
pip install -r requirements.txt
```

---

## Usage

Place the input video inside the `data/` directory.

For example:

```text
data/sample.mp4
```

Run the main program:

```bash
python app/main.py
```

After execution, analysis results will be generated inside:

```text
outputs/
```

---

## Current Development Status

The core video analysis pipeline is functional.

The current version supports:

- Video information extraction
- Frame difference analysis
- Motion event detection
- Shot detection
- Optical flow analysis
- Shot-level motion magnitude calculation
- Shot-level motion stability analysis
- CSV result export
- Motion visualization
- Shot clip export

The project is currently being extended toward more advanced temporal video analysis.

---

## Future Work

Future development will focus on using shot information to improve temporal processing strategies.

Possible directions include:

- Shot-boundary-aware temporal reset
- Shot-level motion context for processing decisions
- Temporal information reuse
- Dynamic processing intervals
- Reducing unnecessary optical flow computation
- Integration with modern optical flow models
- Comparison between traditional and deep-learning-based optical flow methods

The long-term goal is to explore how shot-level motion information can be used to make video motion analysis more efficient and temporally consistent.

---

## Motivation

Modern video analysis often processes frames individually or uses fixed temporal intervals.

However, motion characteristics can vary significantly between shots.

By introducing shot-level motion context, this project explores whether video processing strategies can adapt to different motion conditions instead of treating all frames in the same way.

This project also serves as a practical implementation environment for experimenting with:

- Computer vision
- Video processing
- Optical flow
- Motion analysis
- Modular Python development
- Data visualization

---

## Author

**Nicole Lin**

Graduate Student  
Department of Computer Science and Information Engineering  
National University of Tainan

GitHub:  
https://github.com/nicolelin0523

---

## Repository

https://github.com/nicolelin0523/video-motion-analyzer

