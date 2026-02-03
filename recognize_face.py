import cv2
import face_recognition
import os
import pickle
from datetime import datetime
import csv

# Load known faces
known_encodings = []
known_names = []

for file in os.listdir("data"):
    if file.endswith(".pkl"):
        with open(f"data/{file}", "rb") as f:
            encodings = pickle.load(f)
            known_encodings.append(encodings[0])
            known_names.append(file.replace(".pkl", ""))

cap = cv2.VideoCapture(0)
marked = False

print("Camera started. Press Q to exit.")

while True:
    ret, frame = cap.read()
    if not ret:
        break

    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    locations = face_recognition.face_locations(rgb)
    encodings = face_recognition.face_encodings(rgb, locations)

    for encoding, location in zip(encodings, locations):
        matches = face_recognition.compare_faces(known_encodings, encoding, tolerance=0.5)

        if True in matches and not marked:
            index = matches.index(True)
            name = known_names[index]

            time_now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

            with open("attendance.csv", "a", newline="") as f:
                writer = csv.writer(f)
                writer.writerow([name, time_now])

            print(f"Attendance marked for {name} at {time_now}")
            marked = True

            top, right, bottom, left = location
            cv2.rectangle(frame, (left, top), (right, bottom), (0, 255, 0), 2)
            cv2.putText(frame, name, (left, top - 10),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0), 2)

    cv2.imshow("Face Recognition", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
