import pymysql


class Database:
    def __init__(self):
        self.db = None
        self.cursor = None
        self.connect_to_database()
        self.create_users_table()

    def connect_to_database(self):
        """Connect to the database or create one if it doesn't exist."""
        try:
            self.db = pymysql.connect(
                host="localhost",
                user="CramJam",
                password="snHrHYw4",
                database="CramJamDB"
            )
            self.cursor = self.db.cursor()
        except pymysql.OperationalError as e:
            if e.args[0] == 1049:
                self.create_database()
                self.db = pymysql.connect(
                    host="localhost",
                    user="CramJam",
                    password="snHrHYw4",
                    database="CramJamDB"
                )
                self.cursor = self.db.cursor()
            else:
                raise

    def create_database(self):
        """Create the database if it doesn't exist."""
        self.db = pymysql.connect(
            host="localhost",
            user="CramJam",
            password="snHrHYw4"
        )
        self.cursor = self.db.cursor()
        create_database_query = "CREATE DATABASE IF NOT EXISTS CramJamDB"
        self.cursor.execute(create_database_query)
        self.cursor.close()

    def create_users_table(self):
        """Create a 'users' table if it doesn't exist."""
        create_table_query = """
        CREATE TABLE IF NOT EXISTS users (
            username VARCHAR(50) PRIMARY KEY,
            email VARCHAR(50) NOT NULL,
            password VARCHAR(50) NOT NULL
        )
        """
        self.cursor = self.db.cursor()
        self.cursor.execute(create_table_query)
        self.db.commit()


class Account:
    def __init__(self):
        self.current_user = None
        self.db_manager = Database()

    def register(self, email, username, password):
        try:
            insert_query = "INSERT INTO users (username, email, password) VALUES (%s, %s, %s)"
            self.db_manager.cursor.execute(insert_query, (username, email, password))
            self.db_manager.db.commit()
            print("Registration successful.")
            return username
        except pymysql.IntegrityError:
            print("Username or email already exists. Please choose a different username or email.")

    def login(self, username, password):
        select_query = "SELECT username, password FROM users WHERE username = %s"
        self.db_manager.cursor.execute(select_query, (username,))
        result = self.db_manager.cursor.fetchone()
        if result and result[1] == password:
            print(f"\nWelcome, {username}!")
            return username
        else:
            print("Invalid username or password.")
