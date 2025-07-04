import os
import pickle
import face_recognition

ENCODINGS_PATH = os.path.join('encodings', 'face_encodings.pkl')

# Ensure encodings directory exists
def ensure_dir():
    os.makedirs(os.path.dirname(ENCODINGS_PATH), exist_ok=True)

def load_encodings():
    ensure_dir()
    if not os.path.exists(ENCODINGS_PATH):
        return [], []
    with open(ENCODINGS_PATH, 'rb') as f:
        data = pickle.load(f)
        return data.get('encodings', []), data.get('names', [])

def save_encodings(encodings, names):
    ensure_dir()
    with open(ENCODINGS_PATH, 'wb') as f:
        pickle.dump({'encodings': encodings, 'names': names}, f)

def add_user(name, image_path):
    """Add a new user by encoding their face from an image file."""
    image = face_recognition.load_image_file(image_path)
    encodings = face_recognition.face_encodings(image)
    if not encodings:
        raise ValueError("No face found in the image.")
    face_encoding = encodings[0]
    known_encodings, known_names = load_encodings()
    known_encodings.append(face_encoding)
    known_names.append(name)
    save_encodings(known_encodings, known_names)
    return True 