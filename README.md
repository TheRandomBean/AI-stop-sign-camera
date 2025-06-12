# AI stop detection

AI Stop Detection is a Python program designed to detect when a stop sign has been run. It can be connected to a live camera feed or provided with an MP4 file.


## Installation

To install clone the repo, and then cd into it

```bash
pip install -r requirements.txt
```

## Setting
To configure the 
```yaml
app:
  version: 1.0
  model: yolov8n.pt

camera:
  source: fullstop.mp4 # If using a camera, replace with the camera index (0 for default camera)
  location: cam1
  stop_zone:
  - [266, 275]
  - [375, 247]
  - [340, 233]
  - [233, 250]

detection:
  stop_tolerance: 3

output:
  violation_file: violations.csv

settings:
  use_debug: false # When set true, debug info such as frame count and FPS will be displayed
```
