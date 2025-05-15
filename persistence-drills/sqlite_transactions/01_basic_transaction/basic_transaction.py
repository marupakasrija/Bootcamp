# 01_basic_transaction/basic_transaction.py
import sqlite3
import os

# Define a database file name for this specific demo
DATABASE_NAME = "basic_transaction_demo.db"

def create_connection(db_file):
    """ Creates a database connection """
    conn = None
    try:
        # connect will create the file if it doesn't exist
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
        name TEXT NOT NULL UNIQUE, -- UNIQUE constraint to cause a deliberate error
        quantity INTEGER NOT NULL
    );
    """
    try:
        cursor = conn.cursor()
        cursor.execute(create_items_table_sql)
        conn.commit() # Commit the table creation
        print("Demo table 'items' checked/created.")
    except sqlite3.Error as e:
        print(f"Error setting up demo table: {e}")
        conn.rollback()

def demonstrate_basic_transaction(conn, cause_error=True):
    """
    Demonstrates a transaction with commit or rollback using the connection context manager.
    If cause_error is True, an IntegrityError is introduced.
    """
    items_to_insert_good = [
        ("Item A", 10),
        ("Item B", 25),
        ("Item C", 5),
    ]
    items_to_insert_with_error = [
        ("Item D", 50),
        ("Item E", 15),
        ("Item D", 30), # Duplicate name, will cause IntegrityError
        ("Item F", 100),
    ]

    data_to_use = items_to_insert_with_error if cause_error else items_to_insert_good
    action = "attempting inserts that will cause an error" if cause_error else "performing inserts that should succeed"

    print(f"\n--- Demonstrating Basic Transaction ({action}) ---")
    try:
        # Using 'with conn:' context manager starts a transaction automatically.
        # If the block finishes without exceptions, conn.commit() is called.
        # If an exception occurs, conn.rollback() is called.
        with conn:
            print("Transaction started...")
            cursor = conn.cursor()
            sql = "INSERT INTO items (name, quantity) VALUES (?, ?);"

            for name, quantity in data_to_use:
                print(f"  Executing INSERT for: ({name}, {quantity})")
                cursor.execute(sql, (name, quantity))
                # Changes are staged in the transaction

            print("Transaction block finished (all execute calls successful).")
            # If we reach here, conn.commit() happens automatically upon exiting the 'with' block.

    except sqlite3.Error as e:
        # This block is executed if an error occurs during the transaction.
        # The 'with conn:' context manager has already called rollback.
        print(f"\nCaught an exception during transaction: {e}")
        print("Transaction automatically rolled back by the 'with conn:' context manager.")

    except Exception as e:
        # Catch any other unexpected errors
        print(f"\nCaught an unexpected error during transaction: {e}")
        print("Transaction automatically rolled back by the 'with conn:' context manager.")


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
    # Determine the path for the database file relative to the script's location
    script_dir = os.path.dirname(os.path.abspath(__file__))
    db_path = os.path.join(script_dir, DATABASE_NAME)

    # Clean up the database file for a fresh start each time
    if os.path.exists(db_path):
        os.remove(db_path)
        print(f"Removed existing database: {db_path}")

    conn = create_connection(db_path)

    if conn:
        setup_demo_table(conn)

        # Demonstrate a transaction that will fail and rollback
        demonstrate_basic_transaction(conn, cause_error=True)

        # Optional: Clean the table and demonstrate a successful transaction
        # print("\n--- Clearing table for success demo ---")
        # conn.execute("DELETE FROM items;")
        # conn.commit()
        # demonstrate_basic_transaction(conn, cause_error=False)


        conn.close()
        print(f"\nDatabase connection closed for {DATABASE_NAME}.")
    else:
        print("Failed to create database connection.")