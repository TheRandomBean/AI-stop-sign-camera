# AI stop detection

AI Stop Detection is a Python program designed to detect when a stop sign has been run. It can be connected to a live camera feed or provided with an MP4 file.


## Installation

To install clone the repo, and then cd into it

```bash
pip install -r requirements.txt
```

## Setting
You can modify several settings in the YAML file to change how the script behaves.
```yaml
app:
  version: 1.0
  model: yolov8n.pt

camera:
  source: fullstop.mp4
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
  use_debug: false
```
from example, to change whether the script uses a MP4 file or a camera you can change to 0 (0 is the default camera)

```yaml
camera:
  source: 0
```
