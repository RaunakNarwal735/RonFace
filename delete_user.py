import argparse
from face_db import load_encodings, save_encodings

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Delete a registered user from the face access system.")
    parser.add_argument('--name', required=True, help='Name of the user to delete')
    args = parser.parse_args()

    encodings, names = load_encodings()
    if args.name not in names:
        print(f"User '{args.name}' not found.")
        exit(1)
    # Remove all entries with this name (in case of duplicates)
    new_encodings = [enc for enc, n in zip(encodings, names) if n != args.name]
    new_names = [n for n in names if n != args.name]
    save_encodings(new_encodings, new_names)
    print(f"User '{args.name}' deleted successfully.") 