import cv2

points = []

def click_event(event, x, y, flags, params):
    if event == cv2.EVENT_LBUTTONDOWN:
        points.append((x, y))
        print(f"Point {len(points)}: ({x}, {y})")

# --- Load the first frame of the video ---
video_path = "fullstop.mp4"  # <- change to your actual video file
cap = cv2.VideoCapture(2)

ret, frame = cap.read()
cap.release()

if not ret:
    print("[ERROR] Could not read video frame.")
    exit()

# --- Display the frame and capture points ---
cv2.imshow("Click to define stop zone", frame)
cv2.setMouseCallback("Click to define stop zone", click_event)
cv2.waitKey(0)
cv2.destroyAllWindows()

print("Your STOP_ZONE points:", points)