import openai
import re
import pymysql
import requests

db = pymysql.connect(
    host='localhost',
    user='CramJam',
    password='snHrHYw4',
    database='CramJamDB'
)

# Replace with your API key
api_key = "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"


def is_internet_available():
    try:
        # Attempt to make a simple HTTP GET request to a known website (e.g., google.com)
        response = requests.get("https://platform.openai.com/")
        # Check if the request was successful (status code 200)
        return response.status_code == 200
    except requests.ConnectionError:
        # If there's a connection error, it means there is no internet connection
        return False


def establish_db_connection():
    return pymysql.connect(
        host='localhost',
        user='CramJam',
        password='snHrHYw4',
        database='CramJamDB'
    )


def extract_terms_and_definitions(input_text):
    format_pattern = r'^\d+\.\s*(.+?)\s*:\s*(.+)$'
    lines = input_text.split('\n')
    terms_and_definitions = []

    for line in lines:
        match = re.match(format_pattern, line)
        if match:
            term, definition = match.groups()
            terms_and_definitions.append((term.strip(), definition.strip()))

    return terms_and_definitions


def create_lessons_table(cursor):
    create_table_sql = """
    CREATE TABLE IF NOT EXISTS lessons (
        lessonID int PRIMARY KEY AUTO_INCREMENT,
        owner VARCHAR(50),
        lesson VARCHAR(50),
        public BOOL,
        FOREIGN KEY (owner) REFERENCES users(username)
    )
    """
    cursor.execute(create_table_sql)
    db.commit()


def create_dictionary_table(cursor):
    create_table_sql = """
    CREATE TABLE IF NOT EXISTS dictionary (
        lessonID int,
        term VARCHAR(50) NOT NULL,
        definition VARCHAR(255) NOT NULL,  -- Changed definition to NOT NULL
        FOREIGN KEY (lessonID) REFERENCES lessons(lessonID)
    )
    """
    cursor.execute(create_table_sql)
    db.commit()


def store_in_database(terms_and_definitions, owner, lesson_title, public):
    db = establish_db_connection()
    with db.cursor() as cursor:
        try:
            create_lessons_table(cursor)
            # Insert a new lesson into the 'lessons' table
            sql_lessons = "INSERT INTO lessons (owner, lesson, public) VALUES (%s, %s, %s)"
            cursor.execute(sql_lessons, (owner, lesson_title, public))
            db.commit()

            # Retrieve the lessonID of the inserted lesson
            lessonID = cursor.lastrowid

            create_dictionary_table(cursor)
            # Insert terms and definitions into the 'dictionary' table with the lessonID
            sql_dictionary = "INSERT INTO dictionary (lessonID, term, definition) VALUES (%s, %s, %s)"
            # Check if the definition already exists before inserting
            for term, definition in terms_and_definitions:
                cursor.execute("SELECT definition FROM dictionary WHERE definition = %s", (definition,))
                existing_definition = cursor.fetchone()
                if existing_definition is None:
                    cursor.execute(sql_dictionary, (lessonID, term, definition))
            db.commit()
        except pymysql.MySQLError as e:
            print(f"An error occurred: {e}")
        except Exception as e:
            print(f"An error occurred: {e}")
        finally:
            db.close()


# Learning material
with open("Assets/notes.txt", 'r', encoding='utf-8') as file:
    file_contents = file.read()


def generate_dof(learning_material):
    prompt = f"Create a 20-item list of definitions of terms based on the following information (It should be written in this format <Number>. <term> : <definition>):\n {learning_material}"
    response = openai.Completion.create(
        engine="text-davinci-002",
        prompt=prompt,
        max_tokens=2000,
        api_key=api_key
    )
    return response.choices[0].text.strip()


if is_internet_available():
    DOF = None
    terms_and_definitions = []

    while not terms_and_definitions:  # Loop until terms_and_definitions is not empty
        DOF = generate_dof(file_contents)
        terms_and_definitions = extract_terms_and_definitions(DOF)

    lesson_title = input("Title: ")
    owner = "deo"
    public = 1
    store_in_database(terms_and_definitions, owner, lesson_title, public)
    print(DOF)
    print(terms_and_definitions)
else:
    print("No internet connection.")
