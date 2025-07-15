# Face Recognition Access System

A modular, Windows-compatible face recognition-based access system using Python, OpenCV, and face_recognition. Detects and recognizes faces in real-time from a webcam, allowing user registration and local encoding storage. Designed for easy extension to GUI and hardware (e.g., door lock) integration.

## Why This Model is Better (and How It Works Smoothly on Low-Powered CPUs)

### **1. Efficient, Accurate, and Modular**
- **Built on [face_recognition](https://github.com/ageitgey/face_recognition):**
  - Uses dlib’s deep learning model, which is highly accurate (99.38% on LFW benchmark) and robust in real-world conditions.
  - Supports both HOG (Histogram of Oriented Gradients) and CNN models for face detection. We use HOG for speed on CPUs.
- **Modular Design:**
  - Clean separation of face database, recognition logic, and user registration.
  - Easy to extend with GUI, hardware, or new features.

### **2. Optimized for Low-Powered CPUs**
- **HOG Model for Detection:**
  - The HOG model is much faster than deep CNNs and works well on CPUs, making it ideal for laptops, Raspberry Pi, and other low-power devices.
- **Frame Resizing:**
  - Frames are resized to 1/4 their original size before detection/recognition, reducing computation and increasing speed without sacrificing much accuracy.
- **Process Every Nth Frame:**
  - Recognition/detection is run in the background every few seconds, not every frame, reducing CPU load.
- **Threaded Video Capture:**
  - Video frames are captured in a separate thread, so the UI remains smooth and responsive even if recognition is slow.
- **Background Detection Thread:**
  - Face detection and recognition run in a dedicated background thread, so the main UI and tracking never block or freeze.
- **Face Tracking:**
  - Once a face is detected, OpenCV trackers follow it in real time, so recognition is only needed when a new face appears or tracking is lost.
- **Fallback to Fast Trackers:**
  - The system tries multiple tracker types (KCF, CSRT, MOSSE) for maximum compatibility and speed.

### **3. Seamless User Experience**
- **No UI Freezes:**
  - The main thread always displays the latest frame, and tracking is updated in real time.
- **Instant Registration:**
  - Users can register their face from the webcam with a single key press, and the system updates instantly.
- **Robust to Camera Issues:**
  - Handles black frames, camera disconnects, and other errors gracefully.

### **4. Why This is Better Than Many Alternatives**
- **Most open-source face recognition projects:**
  - Run detection/recognition on every frame, causing lag on CPUs.
  - Don’t use threading or tracking, so the UI freezes during recognition.
  - Are not modular or easy to extend.
- **This project:**
  - Is designed for real-world, low-power, and embedded use.
  - Uses best practices from both computer vision and software engineering.
  - Is easy to adapt for new features, hardware, or platforms.

---

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
2. **Create and activate a virtual environment (recommended):**
   ```bat
   python -m venv venv
   venv\Scripts\activate
   ```
3. **Upgrade pip (recommended):**
   ```bat
   python -m pip install --upgrade pip
   ```
4. **Install dependencies:**
   ```bat
   pip install -r requirements.txt
   ```
5. **(Optional) Ensure your webcam is connected and working.**

## Usage
### 1. Register a New User
Register a user by providing a name and an image file (with a clear face):
```bat
python register_user.py --name "Alice" --image path_to_alice_photo.jpg
```
- The face encoding will be stored locally for future recognition.

### 2. Run Real-Time Recognition
Start the access system:
```bat
python main.py
```
- The webcam feed will open.
- Detected faces will be labeled with the user name and "Access Granted" or "Access Denied".
- Press `q` to quit.

## Virtual Environment: Important Commands
- **Create venv:**
  ```bat
  python -m venv venv
  ```
- **Activate venv:**
  ```bat
  venv\Scripts\activate
  ```
- **Deactivate venv:**
  ```bat
  deactivate
  ```
- **Install requirements:**
  ```bat
  pip install -r requirements.txt
  ```

## Project Structure
```
face_db.py           # Handles encoding storage and user registration
register_user.py     # CLI script to add new users
main.py              # Real-time recognition loop
requirements.txt     # Dependencies
encodings/           # Stores face_encodings.pkl
venv_setup.bat       # Script to set up virtual environment (Windows)
```

## Extending This Project
- **GUI:** Add a Tkinter interface for user registration and status display.
- **Hardware Integration:** Connect to a relay/servo for door lock control (e.g., via GPIO or USB relay).
- **Speed Optimization:** Use HOG model, resize frames, or batch processing for faster recognition on CPU.

## Probable Errors
### CMake Not Installed or Not in PATH (dlib build error)
If you see an error like:
```
CMake is not installed on your system!
ERROR: Failed building wheel for dlib
```
**Solution:**
1. Download and install CMake from [https://cmake.org/download/](https://cmake.org/download/)
2. During installation, select "Add CMake to the system PATH for all users" (or at least for your user).
3. Open a new Command Prompt and run:
   ```bat
   cmake --version
   ```
   You should see the CMake version printed.
4. Retry installing requirements:
   ```bat
   pip install -r requirements.txt
   ```

If you still get errors, ensure you are using a compatible Python version (3.7–3.10 is safest for dlib) and that you have [Build Tools for Visual Studio](https://visualstudio.microsoft.com/visual-cpp-build-tools/) installed if prompted for a C++ compiler.

---
Inspired by [ageitgey/face_recognition](https://github.com/ageitgey/face_recognition). 
