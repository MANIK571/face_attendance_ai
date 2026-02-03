import os
import sys
import pickle
import cv2
import face_recognition
from flask import Flask, render_template, request, jsonify,url_for

from core.user_registration import register_user, delete_user
from core.attendance_manager import punch_in, punch_out, read_attendance
from core.liveness_utils import enhance_low_light, detect_eye_movement, frame_variance_check


# -------------------------------------------------
# PYINSTALLER RESOURCE PATH HELPER
# -------------------------------------------------
def resource_path(relative_path):
    """
    Get absolute path to resource, works for dev and for PyInstaller EXE
    """
    try:
        base_path = sys._MEIPASS  # PyInstaller temp folder
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)


# -------------------------------------------------
# CREATE FLASK APP (ORDER MATTERS)
# -------------------------------------------------
app = Flask(
    __name__,
    template_folder=resource_path("templates"),
    static_folder=resource_path("static")
)


# -------------------------------------------------
# DIRECTORIES (SAFE FOR LOCAL + EXE)
# -------------------------------------------------
USER_IMAGE_DIR = os.path.join(app.static_folder, "user_images")
DATA_DIR = resource_path("data")
TEMP_DIR = os.path.join(resource_path("."), "temp_frames")
FACE_DATA = os.path.join(DATA_DIR, "faces_data.pkl")

os.makedirs(USER_IMAGE_DIR, exist_ok=True)
os.makedirs(DATA_DIR, exist_ok=True)
os.makedirs(TEMP_DIR, exist_ok=True)


# -------------------------------------------------
# ROUTES
# -------------------------------------------------
@app.route("/")
def index():
    users = []

    if os.path.exists(USER_IMAGE_DIR):
        for file in os.listdir(USER_IMAGE_DIR):
            if file.lower().endswith(".jpg"):
                users.append({
                    "name": file.replace(".jpg", ""),
                    "image": url_for("static", filename=f"user_images/{file}")
                })

    attendance = read_attendance()

    return render_template(
        "index.html",
        users=users,
        attendance=attendance
    )


@app.route("/register", methods=["POST"])
def register():
    username = request.form.get("username")
    image = request.files.get("image")

    if not username or not image:
        return jsonify({"status": "error", "message": "Missing data"})

    image_path = os.path.join(USER_IMAGE_DIR, f"{username}.jpg")
    image.save(image_path)

    success, msg = register_user(username, image_path)

    if not success:
        if os.path.exists(image_path):
            os.remove(image_path)
        return jsonify({"status": "error", "message": msg})

    return jsonify({
        "status": "success",
        "message": msg,
        "refresh": True
    })


@app.route("/delete_user", methods=["POST"])
def delete():
    username = request.json.get("username")

    success, msg = delete_user(username)

    image_path = os.path.join(USER_IMAGE_DIR, f"{username}.jpg")
    if os.path.exists(image_path):
        os.remove(image_path)

    return jsonify({
        "status": "success" if success else "error",
        "message": msg,
        "refresh": True
    })


# -------------------------------------------------
# LIVENESS + FACE VALIDATION
# -------------------------------------------------
def validate_live_face(paths):
    images = []
    encodings = []

    sample_paths = paths[::4][:5]  # process only 5 frames

    for path in sample_paths:
        img = cv2.imread(path)
        if img is None:
            continue

        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        img = enhance_low_light(img)

        locs = face_recognition.face_locations(img, model="hog")
        if not locs:
            continue

        enc = face_recognition.face_encodings(img, locs)
        if not enc:
            continue

        images.append(img)
        encodings.append(enc[0])

    if len(images) < 3:
        return False, "Face not stable. Look at camera."

    if not detect_eye_movement(images):
        return False, "No eye movement detected. Blink or move head."

    if not frame_variance_check(encodings):
        return False, "Static image detected (possible spoof)."

    return True, encodings[len(encodings) // 2]


def process_attendance(action):
    if not os.path.exists(FACE_DATA):
        return jsonify({
            "status": "error",
            "message": "No registered users found"
        })

    paths = []

    for i in range(20):
        img = request.files.get(f"image{i}")
        if not img:
            return jsonify({"status": "error", "message": "Frame missing"})

        path = os.path.join(TEMP_DIR, f"frame_{i}.jpg")
        img.save(path)
        paths.append(path)

    try:
        live, result = validate_live_face(paths)
    except Exception:
        return jsonify({
            "status": "error",
            "message": "Processing failed. Try again."
        })

    if not live:
        return jsonify({"status": "error", "message": result})

    encoding = result

    with open(FACE_DATA, "rb") as f:
        known_faces = pickle.load(f)

    for name, known_enc in known_faces.items():
        match = face_recognition.compare_faces(
            [known_enc], encoding, tolerance=0.45
        )

        if match[0]:
            success, msg = punch_in(name) if action == "in" else punch_out(name)
            return jsonify({
                "status": "success" if success else "error",
                "message": msg,
                "refresh": True
            })

    return jsonify({
        "status": "error",
        "message": "Face not recognized"
    })


@app.route("/punch_in", methods=["POST"])
def punchin():
    return process_attendance("in")


@app.route("/punch_out", methods=["POST"])
def punchout():
    return process_attendance("out")


# -------------------------------------------------
# MAIN
# -------------------------------------------------
if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=True)
