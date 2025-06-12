import cv2
import yaml
points = []

def config_load(filename, location, setting):
    with open(filename, "r") as output:
        config = yaml.safe_load(output)
    return config[location][setting]

def represent_list_in_flow_style(dumper, data):
    return dumper.represent_sequence('tag:yaml.org,2002:seq', data, flow_style=True)

yaml.add_representer(list, represent_list_in_flow_style)


def config_save(filename, location, setting, data):
    with open(filename, "r") as f:
        config = yaml.safe_load(f)
    
    if location not in config:
        config[location] = {}
        print(f"[?] Couldn't find location '{location}' in config.yaml")
        print(f"[!] Creating new location '{location}' in config.yaml")
    config[location][setting] = data

    with open(filename, "w") as f:
        yaml.dump(config, f, sort_keys=False)

def click_event(event, x, y, flags, params):
    if event == cv2.EVENT_LBUTTONDOWN:
        points.append([x, y])
        print(f"Point {len(points)}: ({x}, {y})")

video_path = config_load("config.yaml", "camera", "source") 
cap = cv2.VideoCapture(2)

ret, frame = cap.read()
cap.release()

if not ret:
    print("[!] Unable to read video frame. Please check the video source.")
    exit()

# --- Display the frame and capture points ---
cv2.imshow("Click to define stop zone", frame)
cv2.setMouseCallback("Click to define stop zone", click_event)
cv2.waitKey(0)
cv2.destroyAllWindows()

config_save("config.yaml", "camera", "stop_zone", points)
print("[?] STOP_ZONE saved to config.yaml")
print("Your STOP_ZONE points:", points)