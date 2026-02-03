import pickle
import os

DATA_FILE = "faces_data.pkl"


def load_faces():
    if not os.path.exists(DATA_FILE):
        return {}
    with open(DATA_FILE, "rb") as f:
        return pickle.load(f)


def save_faces(data):
    with open(DATA_FILE, "wb") as f:
        pickle.dump(data, f)


def save_face(name, encoding):
    faces = load_faces()

    if name not in faces:
        faces[name] = []

    faces[name].append(encoding)
    save_faces(faces)


def delete_user(name):
    faces = load_faces()
    if name in faces:
        del faces[name]
        save_faces(faces)
