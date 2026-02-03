import os
import pickle
import face_recognition
import numpy as np

DATA_PATH = "data/faces_data.pkl"


def load_faces():
    if os.path.exists(DATA_PATH):
        with open(DATA_PATH, "rb") as f:
            return pickle.load(f)
    return {}


def save_faces(data):
    with open(DATA_PATH, "wb") as f:
        pickle.dump(data, f)


def register_user(username, image_path):
    known_faces = load_faces()

    # Load image
    image = face_recognition.load_image_file(image_path)
    encodings = face_recognition.face_encodings(image)

    if len(encodings) == 0:
        return False, "No face detected"

    new_encoding = encodings[0]

    # 🔒 FACE DUPLICATE CHECK
    for existing_name, existing_encoding in known_faces.items():
        match = face_recognition.compare_faces(
            [existing_encoding], new_encoding, tolerance=0.45
        )
        if match[0]:
            return False, f"Face already registered as '{existing_name}'"

    # 🔒 USERNAME DUPLICATE CHECK
    if username in known_faces:
        return False, "Username already exists"

    known_faces[username] = new_encoding
    save_faces(known_faces)

    return True, "User registered successfully"


def delete_user(username):
    if not os.path.exists(DATA_PATH):
        return False, "No data found"

    with open(DATA_PATH, "rb") as f:
        data = pickle.load(f)

    if username not in data:
        return False, "User not found"

    del data[username]

    with open(DATA_PATH, "wb") as f:
        pickle.dump(data, f)

    return True, "User deleted successfully"
