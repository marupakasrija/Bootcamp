# 04_transactions/simple_transaction.py
import sqlite3
import os

# Define a temporary database file name for this example
DATABASE_NAME = "transaction_demo.db"

def create_connection(db_file):
    """ Creates a database connection """
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        # print(f"Connected to database: {db_file}")
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
        conn.rollback() # Rollback table creation if failed

def demonstrate_transaction(conn):
    """ Demonstrates a transaction with commit and rollback """
    items_to_insert = [
        ("Widget A", 10),
        ("Widget B", 25),
        ("Widget C", 5),
        ("Widget A", 15), # This will cause a UNIQUE constraint error
        ("Widget D", 50),
    ]

    print("\n--- Demonstrating Transaction ---")
    try:
        # By default, isolation_level is '', which means transactions are managed by the database.
        # Using a context manager on the connection ensures commit/rollback.
        # conn.isolation_level = None # Can disable transactions if needed, but usually not.

        with conn: # Use connection as a context manager for transaction
            print("Starting transaction...")
            cursor = conn.cursor()
            sql = "INSERT INTO items (name, quantity) VALUES (?, ?);"

            for name, quantity in items_to_insert:
                print(f"Attempting to insert: ({name}, {quantity})")
                # This will execute the statement, but changes are staged, not saved yet.
                cursor.execute(sql, (name, quantity))
                print(f"  Inserted ({name}, {quantity}) (staged)")

            # If the loop finishes without errors, the 'with' block exits,
            # and conn.commit() is automatically called.
            print("All inserts attempted.")
            # If we reached here, it means the transaction would attempt to commit

    except sqlite3.IntegrityError as ie:
        # If an IntegrityError occurs during execute(), an exception is raised.
        # The 'with conn:' block's __exit__ method will automatically call conn.rollback().
        print(f"\nCaught an error during transaction: {ie}")
        print("Transaction will be rolled back automatically by the 'with' block.")

    except sqlite3.Error as e:
        print(f"\nCaught a database error during transaction: {e}")
        print("Transaction will be rolled back automatically by the 'with' block.")

    except Exception as e:
        print(f"\nCaught an unexpected error during transaction: {e}")
        print("Transaction will be rolled back automatically by the 'with' block.")


    # After the transaction attempt (whether committed or rolled back), check the table state
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


# --- Main Execution ---
if __name__ == "__main__":
    script_dir = os.path.dirname(os.path.abspath(__file__))
    db_path = os.path.join(script_dir, DATABASE_NAME)

    # Clean up the database file for a fresh start
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