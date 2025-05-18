import sqlite3
import os

DATABASE_NAME = "transaction_demo.db"

def create_connection(db_file):
    """ Creates a database connection """
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        return conn
    except sqlite3.Error as e:
        print(f"Error connecting to database: {e}")
        return None

def setup_demo_table(conn):
    """ Creates a simple table for the transaction demo """
    create_items_table_sql = """
    CREATE TABLE IF NOT EXISTS items (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL UNIQUE, -- Unique constraint to cause an error
        quantity INTEGER NOT NULL
    );
    """
    try:
        cursor = conn.cursor()
        cursor.execute(create_items_table_sql)
        conn.commit()
        print("Demo table 'items' checked/created.")
    except sqlite3.Error as e:
        print(f"Error setting up demo table: {e}")
        conn.rollback()

def demonstrate_transaction(conn):
    """ Demonstrates a transaction with commit and rollback """
    items_to_insert = [
        ("Widget A", 10),
        ("Widget B", 25),
        ("Widget C", 5),
        ("Widget A", 15), 
        ("Widget D", 50),
    ]

    print("\n--- Demonstrating Transaction ---")
    try:

        with conn: 
            print("Starting transaction...")
            cursor = conn.cursor()
            sql = "INSERT INTO items (name, quantity) VALUES (?, ?);"

            for name, quantity in items_to_insert:
                print(f"Attempting to insert: ({name}, {quantity})")
                cursor.execute(sql, (name, quantity))
                print(f"  Inserted ({name}, {quantity}) (staged)")

            print("All inserts attempted.")

    except sqlite3.IntegrityError as ie:
        print(f"\nCaught an error during transaction: {ie}")
        print("Transaction will be rolled back automatically by the 'with' block.")

    except sqlite3.Error as e:
        print(f"\nCaught a database error during transaction: {e}")
        print("Transaction will be rolled back automatically by the 'with' block.")

    except Exception as e:
        print(f"\nCaught an unexpected error during transaction: {e}")
        print("Transaction will be rolled back automatically by the 'with' block.")


    print("\n--- Checking Table State After Transaction Attempt ---")
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT id, name, quantity FROM items;")
        rows = cursor.fetchall()
        if rows:
            print("Items currently in the table:")
            for row in rows:
                print(f"ID: {row[0]}, Name: {row[1]}, Quantity: {row[2]}")
        else:
            print("Table is empty.")

        cursor.execute("SELECT COUNT(*) FROM items;")
        count = cursor.fetchone()[0]
        print(f"Total rows in table: {count}")

    except sqlite3.Error as e:
        print(f"Error checking table state: {e}")


if __name__ == "__main__":
    script_dir = os.path.dirname(os.path.abspath(__file__))
    db_path = os.path.join(script_dir, DATABASE_NAME)

    if os.path.exists(db_path):
        os.remove(db_path)
        print(f"Removed existing database: {db_path}")

    conn = create_connection(db_path)

    if conn:
        setup_demo_table(conn)
        demonstrate_transaction(conn)
        conn.close()
        print(f"\nDatabase connection closed for {DATABASE_NAME}.")
    else:
        print("Failed to create database connection.")