import sqlite3

DATABASE = "my_recipes.db"


def get_database_connection():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row  # This allows accessing columns by name
    return conn


def migrate_database():
    conn = get_database_connection()
    cursor = conn.cursor()

    try:
        cursor.execute("PRAGMA table_info(recipes)")
        columns = [column[1] for column in cursor.fetchall()]

        if "image_url" not in columns:
            cursor.execute("ALTER TABLE recipes ADD COLUMN image_url TEXT")
            print("Added image_url column to recipes table")

        if "video_url" not in columns:
            cursor.execute("ALTER TABLE recipes ADD COLUMN video_url TEXT")
            print("Added video_url column to recipes table")

        conn.commit()
    except Exception as e:
        conn.rollback()
        print(f"An error occurred during database migration: {e}")
    finally:
        conn.close()


def init_database():
    conn = get_database_connection()
    cursor = conn.cursor()

    try:
        with open("models/schema.sql", "r") as f:
            schema_sql = f.read()
        cursor.executescript(schema_sql)
        conn.commit()
        print("Database schema loaded successfully from schema.sql")
    except FileNotFoundError:
        print("Error: schema.sql not found. Make sure it's in the same directory.")
    except Exception as e:
        conn.rollback()
        print(f"An error occurred during database initialization: {e}")
    finally:
        conn.close()

    migrate_database()


if __name__ == "__main__":
    init_database()
    print(
        f"Database '{DATABASE}' initialized successfully with users and recipes tables."
    )
