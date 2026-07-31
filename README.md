# Video Motion Analyzer

A Python side project for analyzing motion changes in videos.

## Project Overview

Video Motion Analyzer is a beginner-friendly Python project for analyzing changes between video frames.

The project will gradually include video reading, frame difference calculation, motion score analysis, result export, and visualization.

## Current Progress

* Project folder structure created
* Python virtual environment configured
* Required Python packages installed
* Git repository initialized
* Application entry point completed
* `.gitignore` configured
* `requirements.txt` created
* Video metadata reader completed
* Command-line video path input added
* Basic error handling added

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
│   └── visualization/
│       ├── __init__.py
│       └── plotter.py
├── tests/
│   └── __init__.py
├── data/
├── outputs/
├── .gitignore
├── README.md
└── requirements.txt
```

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

## Run

Run the project from the root folder:

```bash
python -m app.main
```

The terminal should display:

```text
Video Motion Analyzer
Project initialized successfully.
```

## Planned Features

* Read video metadata
* Display video FPS, resolution, frame count, and duration
* Read video frames
* Calculate differences between adjacent frames
* Generate motion scores
* Export analysis results to CSV
* Generate motion curve visualizations
* Add Optical Flow analysis
* Compare different frame intervals
* Add automated tests
* Build a simple user interface

## Technologies

* Python
* OpenCV
* NumPy
* pandas
* Matplotlib
* pytest
* Ruff

## Development Status

This project is currently under development.

The first version focuses on building a clear project structure and implementing basic video motion analysis functions.
