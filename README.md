# Video Motion Analyzer

A Python side project for analyzing visual changes and motion-related information in videos.

## Project Overview

Video Motion Analyzer is a beginner-friendly Python project for analyzing changes between video frames.

The project currently analyzes adjacent video frames using frame differences, brightness changes, and brightness-normalized differences. It also uses shot detection to avoid treating scene transitions as ordinary within-shot motion events.

The goal of this project is to gradually build a structured video analysis pipeline while practicing Python project organization, modular design, Git, data analysis, and computer vision.

## Current Features

- Read video metadata
  - Resolution
  - FPS
  - Frame count
  - Duration
- Read and analyze adjacent video frames
- Calculate original frame difference scores
- Calculate brightness changes
- Calculate brightness-normalized frame differences
- Detect video shots using PySceneDetect
- Remove frame pairs that cross shot boundaries
- Detect high-change events within shots
- Export frame analysis results to CSV
- Export detected events to CSV
- Save important frame pairs and difference images
- Generate motion score curves
- Compare original and brightness-normalized motion curves
- Display an analysis summary in the terminal
- Command-line video input
- Basic error handling

## Analysis Pipeline

```text
Input Video
    ↓
Read Video Metadata
    ↓
Analyze Adjacent Frames
    ↓
Calculate Frame Change Scores
    ↓
Detect Shots
    ↓
Remove Cross-Shot Frame Pairs
    ↓
Detect High-Change Events Within Shots
    ↓
Export CSV / Images / Visualizations
    ↓
Display Analysis Summary
```

## Project Structure

```text
video-motion-analyzer/
├── app/
│   ├── __init__.py
│   └── main.py
├── src/
│   ├── __init__.py
│   ├── video/
│   │   ├── __init__.py
│   │   └── reader.py
│   ├── motion/
│   │   ├── __init__.py
│   │   └── frame_difference.py
│   ├── shots/
│   │   ├── __init__.py
│   │   └── detector.py
│   ├── events/
│   │   ├── __init__.py
│   │   └── detector.py
│   ├── visualization/
│   │   ├── __init__.py
│   │   └── plotter.py
│   └── output/
│       ├── __init__.py
│       └── reporter.py
├── tests/
│   └── __init__.py
├── data/
│   └── .gitkeep
├── outputs/
│   └── .gitkeep
├── .gitignore
├── README.md
└── requirements.txt
```

## Module Responsibilities

### `app/`

Contains the application entry point.

`main.py` connects the different modules and controls the overall analysis pipeline.

### `src/video/`

Handles video reading and metadata extraction.

### `src/motion/`

Calculates frame-based visual change measurements, including:

- Frame difference
- Brightness change
- Brightness-normalized difference

### `src/shots/`

Detects shot boundaries using PySceneDetect and removes frame pairs that cross between different shots.

### `src/events/`

Detects high-change intervals from brightness-normalized frame analysis results within shots.

### `src/visualization/`

Generates motion curves and comparison visualizations.

### `src/output/`

Handles terminal output and displays the analysis summary.

## Installation

### 1. Create a virtual environment

```bash
python -m venv .venv
```

### 2. Activate the virtual environment

On Windows PowerShell:

```powershell
.venv\Scripts\Activate.ps1
```

### 3. Install required packages

```bash
pip install -r requirements.txt
```

## Usage

Place a video file in the `data/` folder.

For example:

```text
data/sample.mp4
```

Run the project from the project root:

```bash
python -m app.main --video data/sample.mp4
```

## Outputs

The analysis results are stored in the `outputs/` folder.

Current outputs include:

```text
outputs/
├── motion_scores.csv
├── events.csv
├── motion_curve.png
├── comparison_curve.png
├── max_change_previous.jpg
├── max_change_current.jpg
├── max_change_difference.jpg
├── max_normalized_change_previous.jpg
├── max_normalized_change_current.jpg
└── max_normalized_change_difference.jpg
```

### `motion_scores.csv`

Stores frame-level analysis results, including original frame changes and brightness-normalized changes.

### `events.csv`

Stores detected high-change events within shots.

### `motion_curve.png`

Visualizes the original frame change scores over time.

### `comparison_curve.png`

Compares original frame change scores with brightness-normalized scores.

## Current Analysis Concept

A large frame difference does not always represent object motion.

For example, global brightness changes or shot transitions can also produce very large differences between adjacent frames.

To reduce these effects, the current pipeline uses two additional steps:

1. **Brightness normalization**

   Reduces the influence of global brightness changes before comparing two frames.

2. **Shot boundary filtering**

   Uses shot detection to prevent frame pairs from different shots from being treated as ordinary motion events.

The current detected events should therefore be interpreted as:

> High visual-change intervals within the same shot.

They do not yet guarantee that the detected change is caused by actual object motion.

## Technologies

- Python
- OpenCV
- NumPy
- pandas
- Matplotlib
- PySceneDetect
- pytest
- Ruff
- Git / GitHub

## Planned Improvements

- Add automated tests
- Add shot-level motion summaries
- Improve event analysis
- Add Optical Flow analysis
- Compare different temporal frame intervals
- Explore more robust motion representations
- Build a simple user interface

## Development Status

This project is currently under development.

The current version provides a shot-aware frame change analysis pipeline. Future development will focus on improving motion interpretation and adding higher-level video analysis features.