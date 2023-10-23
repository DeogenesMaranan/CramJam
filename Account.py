import mysql.connector


class Account:

    def __init__(self):
        self.current_user = None
        self.db = mysql.connector.connect(
            host="localhost",  # Change this to "localhost"
            user="CramJam",
            password="snHrHYw4",
            database="CramJamDB"
        )
        self.cursor = self.db.cursor()
        self.create_users_table()

    def create_users_table(self):
        """Create a 'users' table if it doesn't exist."""
        create_table_query = """
        CREATE TABLE IF NOT EXISTS users (
            id INT AUTO_INCREMENT PRIMARY KEY,
            username VARCHAR(255) NOT NULL,
            email VARCHAR(255) NOT NULL,
            password VARCHAR(255) NOT NULL
        )
        """
        self.cursor.execute(create_table_query)
        self.db.commit()

    @staticmethod
    def __encrypt_password(password):
        """(Private) Encrypts a password using a secret key."""
        __secret_key = "MathintheModernWorld123!@"
        encrypted_password = ""
        for i, char in enumerate(password):
            shift = ord(__secret_key[i % len(__secret_key)]) - ord('a')
            shifted_char = chr((ord(char) - ord('a') + shift) % 26 + ord('a'))
            encrypted_password += shifted_char
        return encrypted_password[::-1]

    def register(self, username, email, password):
        """Prompts the user for creating account info and stores it in the 'users' table. """
        while True:
            encrypted_password = self.__encrypt_password(password)
            try:
                insert_query = "INSERT INTO users (username, email, password) VALUES (%s, %s, %s)"
                self.cursor.execute(insert_query, (username, email, encrypted_password))
                self.db.commit()
                print("Registration successful.")
                return username
            except mysql.connector.IntegrityError:
                print("Username or email already exists. Please choose a different username or email.")

    def login(self, username, password):
        """Prompts the user to log in and checks if it matches a stored user account in the 'users' table. """
        encrypted_password = self.__encrypt_password(password)
        select_query = "SELECT username, password FROM users WHERE username = %s"
        self.cursor.execute(select_query, (username,))
        result = self.cursor.fetchone()
        if result and result[1] == encrypted_password:
            print(f"\nWelcome, {username}!")
            return username
        else:
            print("Invalid username or password.")
