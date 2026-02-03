import cv2
import face_recognition
import pickle
import os

DATA_FILE = "faces_data.pkl"

name = input("Enter NEW user name: ")

# Load existing data safely
if os.path.exists(DATA_FILE):
    with open(DATA_FILE, "rb") as f:
        faces_data = pickle.load(f)
else:
    faces_data = {}

if name in faces_data:
    print("User already exists. Try a new name.")
    exit()

cap = cv2.VideoCapture(0)
encodings = []

print("REGISTRATION MODE ONLY")
print("No recognition will happen")

while len(encodings) < 15:
    ret, frame = cap.read()
    if not ret:
        continue

    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    locations = face_recognition.face_locations(rgb)

    # 🚨 IMPORTANT: only capture, never compare
    if len(locations) == 1:
        encoding = face_recognition.face_encodings(rgb, locations)[0]
        encodings.append(encoding)
        print(f"Captured {len(encodings)}/15")

    cv2.imshow("Register New User", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()

faces_data[name] = encodings

with open(DATA_FILE, "wb") as f:
    pickle.dump(faces_data, f)

print(f"User '{name}' registered successfully.")
