import cv2
import face_recognition
import numpy as np
from scipy.spatial import distance as dist


# -------- LOW LIGHT ENHANCEMENT --------
def enhance_low_light(image):
    ycrcb = cv2.cvtColor(image, cv2.COLOR_RGB2YCrCb)
    y, cr, cb = cv2.split(ycrcb)
    y = cv2.equalizeHist(y)
    merged = cv2.merge([y, cr, cb])
    return cv2.cvtColor(merged, cv2.COLOR_YCrCb2RGB)


# -------- EYE ASPECT RATIO --------
def eye_aspect_ratio(eye):
    A = dist.euclidean(eye[1], eye[5])
    B = dist.euclidean(eye[2], eye[4])
    C = dist.euclidean(eye[0], eye[3])
    return (A + B) / (2.0 * C)


# -------- EYE MOVEMENT / BLINK DETECTION --------
def detect_eye_movement(images):
    ear_values = []

    for img in images:
        landmarks = face_recognition.face_landmarks(img)
        if not landmarks:
            continue

        face = landmarks[0]
        if "left_eye" in face and "right_eye" in face:
            left = eye_aspect_ratio(face["left_eye"])
            right = eye_aspect_ratio(face["right_eye"])
            ear_values.append((left + right) / 2.0)

    if len(ear_values) < 5:
        return False

    # Detect EAR variation
    max_ear = max(ear_values)
    min_ear = min(ear_values)

    # Natural blink / eye movement
    return (max_ear - min_ear) > 0.04


# -------- STATIC IMAGE SPOOF CHECK --------
def frame_variance_check(encodings):
    diffs = []
    for i in range(len(encodings) - 1):
        diffs.append(np.linalg.norm(encodings[i] - encodings[i + 1]))

    # If almost no change across many frames → spoof
    return max(diffs) > 0.008
