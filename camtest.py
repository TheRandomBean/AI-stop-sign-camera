import cv2
import numpy as np
import time
from csv import * 
from ultralytics import YOLO
from ultralytics.utils import LOGGER
LOGGER.setLevel("ERROR")

violationFile = "violations.csv"
cam = "cam1" # proof of concept, will be replaced with camera location
videofile = "fullstop.mp4"
debug = True
car_states = {}  # key = ID, value = {'entered': True, 'stopped': False, 'frames': []}
frame_count = 0
stop_tolerance = 3
cap = cv2.VideoCapture(2)
model = YOLO("yolov8n.pt")

STOP_ZONE = [(266, 275), (375, 247), (340, 233), (233, 250)]
COCO_CLASSES = [
    "person", "bicycle", "car", "motorcycle", "airplane", "bus", "train",
    "truck", "boat", "traffic light", "fire hydrant", "stop sign", "parking meter", "bench",
    "bird", "cat", "dog", "horse", "sheep", "cow", "elephant", "bear", "zebra", "giraffe",
    "backpack", "umbrella", "handbag", "tie", "suitcase", "frisbee", "skis", "snowboard",
    "sports ball", "kite", "baseball bat", "baseball glove", "skateboard", "surfboard",
    "tennis racket", "bottle", "wine glass", "cup", "fork", "knife", "spoon", "bowl",
    "banana", "apple", "sandwich", "orange", "broccoli", "carrot", "hot dog", "pizza",
    "donut", "cake", "chair", "couch", "potted plant", "bed", "dining table", "toilet",
    "tv", "laptop", "mouse", "remote", "keyboard", "cell phone", "microwave", "oven",
    "toaster", "sink", "refrigerator", "book", "clock", "vase", "scissors", "teddy bear",
    "hair drier", "toothbrush"
]


def filewrite(file, frame, obj_id, cam):
    with open(violationFile, 'a', newline='') as csvfile:
        row = [file, frame, obj_id, cam]
        write = writer(csvfile)
        write.writerow(row)
        csvfile.close()
        print("[!] Violation logged")
        pass

# Helper to check if center point is in ROI
def point_in_roi(point, roi_pts):
    return cv2.pointPolygonTest(np.array(roi_pts, dtype=np.int32), point, False) >= 0


while cap.isOpened():
    start_time = time.time()
    ret, frame = cap.read()
    if not ret:
        break

    frame_count += 1
    results = model.track(frame, persist=True, classes=[2, 11])  # class 2 = car

    # Draw ROI
    cv2.polylines(frame, [np.array(STOP_ZONE, dtype=np.int32)], isClosed=True, color=(0, 255, 0), thickness=2)
    if results[0].boxes.id is not None:
        ids = results[0].boxes.id.cpu().numpy().astype(int)
        boxes = results[0].boxes.xywh.cpu().numpy()
        class_ids = results[0].boxes.cls.cpu().numpy().astype(int)
       
            

        for box, obj_id, class_id in zip(boxes, ids, class_ids):
            x, y, w, h = box
            center = (int(x), int(y))
            class_name = COCO_CLASSES[class_id]
            
            if obj_id not in car_states:
                car_states[obj_id] = {
                    'entered': False,
                    'stopped': False,
                    'violated': False,
                    'frames': []
                }   
            color = (
                int(obj_id * 51 % 256),
                int(obj_id * 45 % 256),
                int(obj_id * 34 % 256)
        )
            x1 = int(x - w / 2)
            y1 = int(y - h / 2)
            x2 = int(x + w / 2)
            y2 = int(y + h / 2)
            state = "N/A"
            if obj_id in car_states:
                if car_states[obj_id]['entered']:
                    state = "Entered"
                if car_states[obj_id]['stopped']:
                    state = "Stopped"
                if car_states[obj_id]['entered'] and not car_states[obj_id]['stopped'] and not point_in_roi(center, STOP_ZONE):
                    state = "Violated"
                    color = (5, 5, 255)
            cv2.rectangle(frame, (x1, y1), (x2, y2), color, 1)
            #cv2.circle(frame, center, 4, (255, 0, 0), -1)
            

            cv2.putText(frame, f'ID: {obj_id}, State: {state}, obj: {class_name}', (x1, y1 - 10),
            cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 1)

            # Track car entry into stop zone
            if point_in_roi(center, STOP_ZONE):
                car_states[obj_id]['frames'].append(center)

                if not car_states[obj_id]['entered']:
                    car_states[obj_id]['entered'] = True

                # Detect stopping by checking minimal movement over 10 frames
                if len(car_states[obj_id]['frames']) > 10:
                    dx = np.std([pt[0] for pt in car_states[obj_id]['frames'][-10:]])
                    dy = np.std([pt[1] for pt in car_states[obj_id]['frames'][-10:]])
                    if dx < 3 and dy < 3:  # Minimal movement
                        car_states[obj_id]['stopped'] = True
            else:
                # Outside ROI, check for violation
                if car_states[obj_id]['entered'] and not car_states[obj_id]['stopped']:
                    cv2.putText(frame, f'violation {obj_id}', (int(x), int(y)), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 0, 0), 2)
                    print(f"[!] Car {obj_id} ran stop sign at frame {frame_count}")
                    filewrite(videofile, frame_count, obj_id, cam)
                    cv2.polylines(frame, [np.array(STOP_ZONE, dtype=np.int32)], isClosed=True, color=(0, 0, 255), thickness=2)
                    car_states[obj_id]['stopped'] = True  # Avoid duplicate logs
                    cv2.imshow("Violation Frame", frame)
                    cv2.waitKey(2000)

    # Show video
    end_time = time.time()
    fps = 1 / (end_time - start_time + 1e-8)  # Avoid division by zero

    if debug == True:    
        cv2.putText(frame, f"FPS: {fps:.2f}", (10, 30),
        cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2)
        cv2.putText(frame, f"Frame: {frame_count}", (10, 50),
        cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2)
    
    cv2.imshow("Stop Sign Detection", frame)
    if cv2.waitKey(1) == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
