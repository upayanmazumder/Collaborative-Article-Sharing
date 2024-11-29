import argparse
from auth import authenticate_user

def main():
    parser = argparse.ArgumentParser(description="CLI tool for user authentication via browser.")
    parser.add_argument(
        "action",
        choices=["authenticate"],
        help="Action to perform. Currently only supports 'authenticate'."
    )
    parser.add_argument("-e", "--email", help="Email address of the user.")
    args = parser.parse_args()

    if not args.email:
        print("Email is required.")
        email = input("Enter email: ")
    else:
        email = args.email

    if args.action == "authenticate":
        authenticate_user(email)

if __name__ == "__main__":
    main()
