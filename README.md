# AI stop detection

**AI Stop Detection** is a Python application that uses computer vision to detect stop sign violations. It can process either a live camera feed or an MP4 video file.


## Installation

To install clone the repo, and then cd into it (Note if you do not have python installed you must install it.)

```bash
git clone https://github.com/TheRandomBean/AI-stop-sign-camera
cd AI-stop-sign-camera
pip install -r requirements.txt
```

## Usage

Before running the camtest.py you first need to [change the source](https://github.com/TheRandomBean/AI-stop-sign-camera?tab=readme-ov-file#switching-input-sources) in the settings, once done run the pointgrabber.py file, and then select the points for your stopping zone. once you have clicked all 4 points, run the camtest.py you should see the window pop up, and your stop zone drawn.

## Setting
You can modify several settings in the YAML file to change how the script behaves.
```yaml
app:
  version: 1.0
  model: yolov8n.pt
camera:
  source: fullstop.mp4
  location: cam1
  stop_zone: [[139, 116], [273, 37], [420, 171], [313, 307]]
detection:
  stop_tolerance: 3
output:
  violation_file: violations.csv
settings:
  use_debug: false
```
## Switching Input Sources
To use a live camera instead of a video file, set the camera.source to 0:

```yaml
camera:
  source: 0
```
## Output
All detected stop sign violations are logged to a CSV file specified in the configuration default violations.csv.

You can change the output file name in the YAML config:

```yaml
output:
  violation_file: violations.csv
```
**Note:** files must remain as a CSV file, if not provided one the script will provide an error.

## Images
![preview_violation](https://github.com/user-attachments/assets/10a26197-24a3-45ee-954b-8be1339b0f97)

