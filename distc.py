import cv2
import cvzone
import dlib
import numpy as np
import math
import sys
from renderFace import renderFace
from cvzone.FaceDetectionModule import FaceDetector


# --- SETTINGS ---
PREDICTOR_PATH = "C:\shape_predictor_68_face_landmarks.dat"


RESIZE_HEIGHT = 480
SKIP_FRAMES = 2
KNOWN_WIDTH = 16  # cm
FOCAL_LENGTH = 500


# Initialize dlib's models
face_detector_dlib = dlib.get_frontal_face_detector()
landmark_predictor = dlib.shape_predictor(PREDICTOR_PATH)

# Initialize cvzone face detector
face_detector_cvzone = FaceDetector(minDetectionCon=0.75)


cap = cv2.VideoCapture(0)

# Check if camera is opened
if not cap.isOpened():
    print("Unable to connect to camera")
    sys.exit()

# Placeholder values
fps = 30.0
ret, im = cap.read()
if not ret:
    print("Unable to read frame")
    sys.exit()

height = im.shape[0]
RESIZE_SCALE = float(height) / RESIZE_HEIGHT
size = im.shape[0:2]

# Frame counter for fps calc
t = cv2.getTickCount()
frame_count = 0

# Main loop
while True:
    if frame_count == 0:
        t = cv2.getTickCount()

    success, img = cap.read()
    if not success:
        break

    # Resize + RGB conversion for dlib
    imDlib = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    imSmall = cv2.resize(img, None, fx=1.0/RESIZE_SCALE, fy=1.0/RESIZE_SCALE, interpolation=cv2.INTER_LINEAR)
    imSmallDlib = cv2.cvtColor(imSmall, cv2.COLOR_BGR2RGB)

    # cvzone face detection
    img, bboxs = face_detector_cvzone.findFaces(img)

    # Dlib face detection (every SKIP_FRAMES)
    if frame_count % SKIP_FRAMES == 0:
        faces = face_detector_dlib(imSmallDlib, 0)

    # Loop over dlib-detected faces for landmarks
    for face in faces:
        newRect = dlib.rectangle(int(face.left() * RESIZE_SCALE),
                                 int(face.top() * RESIZE_SCALE),
                                 int(face.right() * RESIZE_SCALE),
                                 int(face.bottom() * RESIZE_SCALE))

        shape = landmark_predictor(imDlib, newRect)
        renderFace(img, shape)  # draw landmarks

    # Loop over cvzone-detected faces for bbox/distance
    if bboxs:
        for bbox in bboxs:
            x, y, w, h = bbox['bbox']
            center = bbox['center']
            distance = (KNOWN_WIDTH * FOCAL_LENGTH) / w
            cvzone.putTextRect(img, f"Distance: {int(distance)} cm", (x, y - 20), scale=2)
            cvzone.cornerRect(img, (x, y, w, h))
            cv2.circle(img, center, 5, (255, 0, 255), cv2.FILLED)

    # Calculate FPS every 100 frames
    frame_count += 1
    if frame_count == 100:
        t = (cv2.getTickCount() - t) / cv2.getTickFrequency()
        fps = 100.0 / t
        frame_count = 0

    # Show FPS
    cv2.putText(img, f"{fps:.2f} FPS", (50, size[0] - 50), cv2.FONT_HERSHEY_COMPLEX, 1.5, (0, 0, 255), 3)

    # Display
    cv2.imshow("Face Distance + Landmarks", img)

    # Quit
    key = cv2.waitKey(1) & 0xFF
    if key == 27:  # ESC
        break

cap.release()
cv2.destroyAllWindows()
