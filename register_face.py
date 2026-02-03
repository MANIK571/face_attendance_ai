import cv2
import face_recognition
import pickle
import os

DATA_FILE = "faces_data.pkl"

name = input("Enter new user name: ")

# Step 1: Load existing data (if any)
if os.path.exists(DATA_FILE):
    with open(DATA_FILE, "rb") as f:
        faces_data = pickle.load(f)
else:
    faces_data = {}

if name in faces_data:
    print("User already exists!")
    exit()

# Step 2: Capture face encodings
cap = cv2.VideoCapture(0)
encodings = []

print("Look at the camera. Capturing face data...")

while len(encodings) < 20:
    ret, frame = cap.read()
    if not ret:
        continue

    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    locations = face_recognition.face_locations(rgb)

    if len(locations) == 1:
        encoding = face_recognition.face_encodings(rgb, locations)[0]
        encodings.append(encoding)
        print(f"Captured {len(encodings)}/20")

    cv2.imshow("Register User", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()

# Step 3: Add new user to dictionary
faces_data[name] = encodings

# Step 4: Save back to pickle
with open(DATA_FILE, "wb") as f:
    pickle.dump(faces_data, f)

print(f"User '{name}' registered successfully!")
