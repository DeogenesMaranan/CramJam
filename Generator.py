import openai
import re
import pymysql

db = pymysql.connect(
    host='localhost',
    user='CramJam',
    password='snHrHYw4',
    database='CramJamDB'
)

# Replace with your API key
api_key = "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"

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

def create_table_if_not_exists(cursor, table_name, create_table_sql):
    cursor.execute(f"CREATE TABLE IF NOT EXISTS {table_name} {create_table_sql}")
    db.commit()

def create_lessons_table(cursor):
    create_table_sql = """
    CREATE TABLE IF NOT EXISTS lessons (
        owner VARCHAR(50),
        lesson VARCHAR(50) PRIMARY KEY,
        public BOOL,
        FOREIGN KEY (owner) REFERENCES users(username)
    )
    """
    cursor.execute(create_table_sql)
    db.commit()

def create_dictionary_table(cursor):
    create_table_sql = """
    CREATE TABLE IF NOT EXISTS dictionary (
        lesson VARCHAR(50),
        term VARCHAR(50) NOT NULL,
        definition VARCHAR(255) PRIMARY KEY,
        FOREIGN KEY (lesson) REFERENCES lessons(lesson)
    )
    """
    cursor.execute(create_table_sql)
    db.commit()


def store_in_database(terms_and_definitions, owner, lesson_title, public):
    db = establish_db_connection()
    with db.cursor() as cursor:
        try:
            create_lessons_table(cursor)
            sql = "INSERT INTO lessons (owner, lesson, public) VALUES (%s, %s, %s)"
            cursor.execute(sql, (owner, lesson_title, public))

            create_dictionary_table(cursor)
            sql = "INSERT INTO dictionary (lesson, term, definition) VALUES (%s, %s, %s)"
            cursor.executemany(sql, [(lesson_title, term, definition) for term, definition in terms_and_definitions])
            db.commit()
        except pymysql.MySQLError as e:
            print(f"An error occurred: {e}")
        except Exception as e:
            print(f"An error occurred: {e}")
        finally:
            db.close()


# Learning material
with open("notes.txt", 'r', encoding='utf-8') as file:
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


terms_and_definitions = []

#while not terms_and_definitions:  # Loop until terms_and_definitions is not empty

DOF = generate_dof(file_contents)
terms_and_definitions = extract_terms_and_definitions(DOF)

lesson_title = input("Title: ")
owner = "deo"
public = 1
store_in_database(terms_and_definitions, owner, lesson_title, public)
print(DOF)
print(terms_and_definitions)
