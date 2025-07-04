import cv2
import face_recognition
import numpy as np
from face_db import load_encodings, save_encodings
import threading
import time

class VideoCaptureThread:
    def __init__(self, src=0):
        self.cap = cv2.VideoCapture(src)
        self.ret, self.frame = self.cap.read()
        self.running = True
        self.lock = threading.Lock()
        self.thread = threading.Thread(target=self.update, daemon=True)
        self.thread.start()

    def update(self):
        while self.running:
            ret, frame = self.cap.read()
            with self.lock:
                self.ret = ret
                self.frame = frame
            time.sleep(0.01)

    def read(self):
        with self.lock:
            return self.ret, self.frame.copy() if self.ret and self.frame is not None else (False, None)

    def release(self):
        self.running = False
        self.thread.join()
        self.cap.release()

def create_tracker():
    tracker = getattr(cv2, 'TrackerKCF_create', None)
    if tracker is not None:
        return tracker()
    legacy = getattr(cv2, 'legacy', None)
    if legacy is not None:
        tracker = getattr(legacy, 'TrackerKCF_create', None)
        if tracker is not None:
            return tracker()
    tracker = getattr(cv2, 'TrackerCSRT_create', None)
    if tracker is not None:
        return tracker()
    if legacy is not None:
        tracker = getattr(legacy, 'TrackerCSRT_create', None)
        if tracker is not None:
            return tracker()
    raise RuntimeError('No compatible tracker (KCF/CSRT) available in your OpenCV build.')

class DetectionThread(threading.Thread):
    def __init__(self, video, known_encodings, known_names, shared_data, lock, interval=2.0):
        super().__init__(daemon=True)
        self.video = video
        self.known_encodings = known_encodings
        self.known_names = known_names
        self.shared_data = shared_data
        self.lock = lock
        self.interval = interval
        self.running = True

    def run(self):
        while self.running:
            ret, frame = self.video.read()
            if not ret or frame is None:
                time.sleep(0.1)
                continue
            rgb_frame = frame[:, :, ::-1]
            small_frame = cv2.resize(rgb_frame, (0, 0), fx=0.25, fy=0.25)
            face_locations = face_recognition.face_locations(small_frame, model='hog')
            try:
                face_encodings = face_recognition.face_encodings(small_frame, face_locations)
            except Exception as e:
                print("Error during face encoding:", e)
                time.sleep(self.interval)
                continue
            face_locations = [(top*4, right*4, bottom*4, left*4) for (top, right, bottom, left) in face_locations]
            new_trackers = []
            tracked_names = []
            tracked_status = []
            for (top, right, bottom, left), face_encoding in zip(face_locations, face_encodings):
                matches = face_recognition.compare_faces(self.known_encodings, face_encoding)
                name = "Unknown"
                status = "Access Denied"
                if True in matches:
                    first_match_index = matches.index(True)
                    name = self.known_names[first_match_index]
                    status = "Access Granted"
                tracker = create_tracker()
                tracker.init(frame, (left, top, right - left, bottom - top))
                new_trackers.append(tracker)
                tracked_names.append(name)
                tracked_status.append(status)
            with self.lock:
                self.shared_data['trackers'] = new_trackers
                self.shared_data['tracked_names'] = tracked_names
                self.shared_data['tracked_status'] = tracked_status
                self.shared_data['last_update'] = time.time()
            time.sleep(self.interval)

    def stop(self):
        self.running = False

def recognize_face():
    known_encodings, known_names = load_encodings()
    if not known_encodings:
        print("No known faces. Please register users first or use 't' to train.")
    video = VideoCaptureThread(0)
    print("Press 'q' to quit. Press 't' to train/register your face.")
    shared_data = {'trackers': [], 'tracked_names': [], 'tracked_status': [], 'last_update': 0}
    lock = threading.Lock()
    detection_thread = DetectionThread(video, known_encodings, known_names, shared_data, lock, interval=2.0)
    detection_thread.start()
    try:
        while True:
            ret, frame = video.read()
            if not ret or frame is None:
                print("Frame not received from webcam.")
                continue
            if not isinstance(frame, np.ndarray):
                continue
            frame_np = np.asarray(frame, dtype=np.float32)
            if len(frame.shape) != 3 or frame.shape[2] != 3 or np.mean(frame_np) < 5:
                cv2.imshow("Face Access", frame)
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    break
                continue
            # Update trackers and draw boxes
            with lock:
                trackers = shared_data['trackers']
                tracked_names = shared_data['tracked_names']
                tracked_status = shared_data['tracked_status']
            new_boxes = []
            for i, tracker in enumerate(trackers):
                ok, box = tracker.update(frame)
                if ok:
                    (x, y, w, h) = [int(v) for v in box]
                    new_boxes.append((y, x + w, y + h, x))
                else:
                    new_boxes.append(None)
            zipped = list(zip(new_boxes, tracked_names, tracked_status, trackers))
            zipped = [z for z in zipped if z[0] is not None]
            if zipped:
                new_boxes, tracked_names, tracked_status, trackers = zip(*zipped)
                new_boxes = list(new_boxes)
                tracked_names = list(tracked_names)
                tracked_status = list(tracked_status)
                trackers = list(trackers)
            else:
                new_boxes, tracked_names, tracked_status, trackers = [], [], [], []
            for (top, right, bottom, left), name, status in zip(new_boxes, tracked_names, tracked_status):
                color = (0, 255, 0) if status == "Access Granted" else (0, 0, 255)
                cv2.rectangle(frame, (left, top), (right, bottom), color, 2)
                cv2.putText(frame, f"{name}: {status}", (left, top - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.8, color, 2)
            cv2.imshow("Face Access", frame)
            key = cv2.waitKey(1) & 0xFF
            if key == ord('q'):
                break
            elif key == ord('t'):
                # Train/register the first detected face in the frame
                # Run detection immediately for registration
                detection_thread.stop()
                detection_thread.join()
                rgb_frame = frame[:, :, ::-1]
                small_frame = cv2.resize(rgb_frame, (0, 0), fx=0.25, fy=0.25)
                face_locations = face_recognition.face_locations(small_frame, model='hog')
                try:
                    face_encodings = face_recognition.face_encodings(small_frame, face_locations)
                except Exception as e:
                    print("Error during face encoding:", e)
                    continue
                if face_encodings:
                    user_name = input("Enter your name for registration: ").strip()
                    if user_name:
                        known_encodings.append(face_encodings[0])
                        known_names.append(user_name)
                        save_encodings(known_encodings, known_names)
                        print(f"User '{user_name}' registered from webcam.")
                    else:
                        print("Name cannot be empty. Registration cancelled.")
                else:
                    print("No face detected for training. Please try again.")
                # Restart detection thread with updated encodings
                detection_thread = DetectionThread(video, known_encodings, known_names, shared_data, lock, interval=2.0)
                detection_thread.start()
    finally:
        detection_thread.stop()
        detection_thread.join()
        video.release()
        cv2.destroyAllWindows()

if __name__ == "__main__":
    recognize_face() 