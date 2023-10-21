import os
import time
import sys


class Account:

    def __init__(self):
        self.current_user = None
        self.record = {}
        self.users = self.load_users

    @staticmethod
    def __encrypt_password(password):
        """(Private) Encrypts a password using a secret key."""
        __secret_key = "MathintheModernWorld123!@"
        encrypted_password = ""
        for i, char in enumerate(password):  # Shifts each character by certain amount depending on the '__secret_key'
            shift = ord(__secret_key[i % len(__secret_key)]) - ord('a')
            shifted_char = chr((ord(char) - ord('a') + shift) % 26 + ord('a'))
            encrypted_password += shifted_char
        return encrypted_password[::-1]

    @property
    def load_users(self):
        """Loads user account information from the 'accounts' file into the 'users' dict."""
        file_path = os.path.join(os.getcwd(), 'resources', 'accounts')
        try:
            users = {}
            with open(file_path, 'r') as file:
                for line in file:
                    username, encrypted_password = line.strip().split(':')
                    users[username] = {'password': encrypted_password}
            return users
        except FileNotFoundError:
            print("The 'accounts' file is missing.")
            print("Please download the latest version of the Repository")
            time.sleep(3)
            sys.exit(1002)

    def register(self):
        """Prompts user for creating account info and stores it in 'users' dict and 'accounts' file. """
        while True:
            username = input("Enter your username: ")
            if username in self.users:
                print("Username already exists. Please choose a different username.")
            else:
                break
        password = input("Enter a password: ")
        encrypted_password = self.__encrypt_password(password)
        self.users[username] = {'password': encrypted_password}
        file_path = os.path.join(os.getcwd(), 'resources', "accounts")
        with open(file_path, 'a') as file:
            file.write(f"{username}:{encrypted_password}\n")
        print("Registration successful.")
        return username

    def login(self):
        """Prompts the user to login and checks if it matches a stored user account in the 'user' dict. """
        username = input("Enter your username: ")
        password = input("Enter your password: ")
        encrypted_password = self.__encrypt_password(password)
        if username in self.users and self.users[username]['password'] == encrypted_password:
            print(f"\nWelcome, {username}!")
            return username
        else:
            print("Invalid username or password..")
