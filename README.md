# Face Recognition Access System

A modular, Windows-compatible face recognition-based access system using Python, OpenCV, and face_recognition. Detects and recognizes faces in real-time from a webcam, allowing user registration and local encoding storage. Designed for easy extension to GUI and hardware (e.g., door lock) integration.

## Features
- Real-time face detection and recognition via webcam
- Register new users with name and image (CLI)
- Stores face encodings locally (`encodings/face_encodings.pkl`)
- Outputs "Access Granted" or "Access Denied" on video feed
- Modular codebase for easy extension (GUI, hardware)

## Requirements
- Windows (tested on Python 3.10+)
- Python packages:
  - face_recognition
  - dlib
  - opencv-python
  - numpy
  - (tkinter for GUI, included with standard Python on Windows)

## Setup
1. **Clone or download this repository.**
2. **Install dependencies:**
   ```
   pip install -r requirements.txt
   ```
3. **(Optional) Ensure your webcam is connected and working.**

## Usage
### 1. Register a New User
Register a user by providing a name and an image file (with a clear face):
```bash
python register_user.py --name "Alice" --image path_to_alice_photo.jpg
```
- The face encoding will be stored locally for future recognition.

### 2. Run Real-Time Recognition
Start the access system:
```bash
python main.py
```
- The webcam feed will open.
- Detected faces will be labeled with the user name and "Access Granted" or "Access Denied".
- Press `q` to quit.

## Project Structure
```
face_db.py           # Handles encoding storage and user registration
register_user.py     # CLI script to add new users
main.py              # Real-time recognition loop
requirements.txt     # Dependencies
encodings/           # Stores face_encodings.pkl
```

## Extending This Project
- **GUI:** Add a Tkinter interface for user registration and status display.
- **Hardware Integration:** Connect to a relay/servo for door lock control (e.g., via GPIO or USB relay).
- **Speed Optimization:** Use HOG model, resize frames, or batch processing for faster recognition on CPU.

## Notes
- All face data is stored locally; no cloud or network required.
- For best results, use high-quality, front-facing images for registration.

---
Inspired by [ageitgey/face_recognition](https://github.com/ageitgey/face_recognition). 