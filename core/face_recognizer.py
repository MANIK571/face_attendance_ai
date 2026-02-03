import face_recognition
from core.face_store import load_faces

def recognize_face(rgb_frame, tolerance=0.5):
    faces_data = load_faces()
    if not faces_data:
        return None

    known_encodings = []
    known_names = []

    for name, enc_list in faces_data.items():
        for enc in enc_list:
            known_encodings.append(enc)
            known_names.append(name)

    locations = face_recognition.face_locations(rgb_frame)
    encodings = face_recognition.face_encodings(rgb_frame, locations)

    for encoding in encodings:
        matches = face_recognition.compare_faces(
            known_encodings, encoding, tolerance=tolerance
        )
        if True in matches:
            index = matches.index(True)
            return known_names[index]

    return None
