import cv2
import face_recognition
import os

from core.face_store import load_faces, save_face

IMAGE_DIR = "static/user_images"


def register_face_camera(username):
    os.makedirs(IMAGE_DIR, exist_ok=True)

    cap = cv2.VideoCapture(0)
    faces = load_faces()

    while True:
        ret, frame = cap.read()
        if not ret:
            continue

        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        encodings = face_recognition.face_encodings(rgb)

        if encodings:
            new_encoding = encodings[0]

            # Prevent duplicate face registration
            for name, known_encs in faces.items():
                matches = face_recognition.compare_faces(
                    known_encs, new_encoding, tolerance=0.45
                )
                if True in matches:
                    cap.release()
                    cv2.destroyAllWindows()
                    return False, f"Face already registered as {name}"

            # Save face and image
            save_face(username, new_encoding)
            cv2.imwrite(f"{IMAGE_DIR}/{username}.jpg", frame)

            cap.release()
            cv2.destroyAllWindows()
            return True, f"{username} registered successfully"

        cv2.imshow("Register User - Look at Camera", frame)
        if cv2.waitKey(1) & 0xFF == ord("q"):
            break

    cap.release()
    cv2.destroyAllWindows()
    return False, "Registration cancelled"
