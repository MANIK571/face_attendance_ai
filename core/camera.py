import cv2
from core.face_recognizer import recognize_face
from core.image_utils import enhance_brightness


def capture_and_recognize(timeout=10):
    """
    Opens camera, enhances brightness,
    returns recognized name or None
    """

    cap = cv2.VideoCapture(0)

    if not cap.isOpened():
        print("[ERROR] Camera not accessible")
        return None

    print("[INFO] Camera started for recognition. Press Q to cancel.")

    recognized_name = None
    start_time = cv2.getTickCount()

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        # 🔆 Fix low brightness
        frame = enhance_brightness(frame)

        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        name = recognize_face(rgb)

        if name:
            recognized_name = name
            print(f"[INFO] Recognized: {name}")
            break

        cv2.imshow("Camera - Face Recognition", frame)

        if cv2.waitKey(1) & 0xFF == ord("q"):
            break

        # ⏱ timeout protection
        elapsed = (cv2.getTickCount() - start_time) / cv2.getTickFrequency()
        if elapsed > timeout:
            print("[INFO] Camera timeout")
            break

    cap.release()
    cv2.destroyAllWindows()
    return recognized_name
