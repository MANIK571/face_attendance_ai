# Face Authentication Attendance System

## Overview
This project implements a **Face Authentication–Based Attendance System** using real-time webcam input.  
Users can register their face and mark attendance using **Punch In** and **Punch Out** actions.

The system is designed for **attendance use-cases** such as classrooms or offices, focusing on practicality rather than high-security biometric authentication.

---
## DemoLink : https://drive.google.com/file/d/1ssLhZhiHDFKc6uFbYhFzrxY3LNF4HYmn/view?usp=drive_link

## Features
- Face registration using webcam
- Real-time face authentication
- Punch In / Punch Out attendance marking
- Attendance records with date and time
- Display of registered users
- Attendance table in UI
- Basic liveness detection
- Improved handling of low-light conditions

---

## System Workflow
1. User registers by capturing their face through webcam.
2. Facial features are extracted and stored.
3. During Punch In / Punch Out:
   - Live frames are captured
   - Face authentication is performed
   - Attendance is recorded with timestamp
4. Attendance records are displayed on the interface.

---

## Model and Approach Used
The system uses a **pre-trained face recognition model** provided by the `face_recognition` library (dlib-based).

Each detected face is converted into a **128-dimensional face embedding**.  
Authentication is performed by comparing the distance between stored and live embeddings using **Euclidean distance**.

A fixed threshold (`tolerance = 0.45`) is used to determine identity matching.

No custom model training is performed.

---

## Training Process
This project does not involve traditional model training.

- During registration, facial embeddings are generated and stored.
- During authentication, live embeddings are compared with stored embeddings.
- The pre-trained model remains unchanged.

This allows new users to be added without retraining.

---

## Accuracy Expectations
- Good lighting and frontal face: **90–95%**
- Normal indoor conditions: **85–90%**
- Low light or partial occlusion: **75–85%**

The system prioritizes avoiding incorrect user identification, which may occasionally reject valid users.

---

## Liveness Detection
Basic spoof prevention is implemented using:
- Multi-frame capture
- Eye movement / blink detection
- Frame-to-frame variation analysis

This reduces simple spoofing attempts using photos or phone screens.

---

## Known Failure Cases
- Extremely low lighting conditions
- Face partially covered by mask or hand
- Significant changes in facial appearance
- Identical twins or very similar faces
- Low-quality webcam input

These limitations are acceptable for attendance applications.

---

## Technology Stack
- Python
- Flask
- OpenCV
- face_recognition (dlib)
- HTML, CSS
- CSV / local file storage

---

## How to Run Locally

### 1. Clone the repository
```bash
git clone https://github.com/your-username/face-attendance-ai.git
cd face-attendance-ai
