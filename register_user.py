import argparse
from face_db import add_user

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Register a new user for face access system.")
    parser.add_argument('--name', required=True, help='Name of the user')
    parser.add_argument('--image', required=True, help='Path to the image file of the user')
    args = parser.parse_args()

    try:
        add_user(args.name, args.image)
        print(f"User '{args.name}' registered successfully.")
    except Exception as e:
        print(f"Failed to register user: {e}") 