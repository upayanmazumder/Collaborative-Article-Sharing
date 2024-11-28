import argparse
from auth import signup_user, login_user

def prompt_for_credentials():
    """
    Prompts the user for email and password if not provided via command-line arguments.
    """
    email = input("Enter email: ")
    password = input("Enter password: ")
    return email, password

def main():
    parser = argparse.ArgumentParser(description="CLI tool for user authentication.")
    parser.add_argument(
        "action",
        choices=["signup", "login"],
        help="Action to perform. Choose either 'signup' or 'login'."
    )
    parser.add_argument("-e", "--email", help="Email address of the user.")
    parser.add_argument("-p", "--password", help="Password for the user.")
    args = parser.parse_args()

    # If email or password are not provided via command-line, ask for them interactively.
    if not args.email or not args.password:
        print("Email and/or password not provided via command-line arguments.")
        email, password = prompt_for_credentials()
    else:
        email, password = args.email, args.password

    if args.action == "signup":
        signup_user(email, password)
    elif args.action == "login":
        login_user(email, password)

if __name__ == "__main__":
    main()
