import cv2
from core.face_recognizer import recognize_face
from core.attendance_manager import mark_attendance

action = input("Enter action (IN / OUT): ").strip().upper()

if action not in ["IN", "OUT"]:
    print("Invalid action")
    exit()

cap = cv2.VideoCapture(0)
marked = False

print("Camera started. Press Q to quit.")

while True:
    ret, frame = cap.read()
    if not ret:
        break

    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    name = recognize_face(rgb)

    if name and not marked:
        mark_attendance(name, action)
        print(f"{action} marked for {name}")
        marked = True

    cv2.imshow("Attendance Camera", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
