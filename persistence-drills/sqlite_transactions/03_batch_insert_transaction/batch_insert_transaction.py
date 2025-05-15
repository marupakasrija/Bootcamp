# 03_batch_insert_transaction/batch_insert_transaction.py
import sqlite3
import os
import time

# Define a database file name for this specific demo
DATABASE_NAME = "batch_insert_transaction_demo.db"

def create_connection(db_file):
    """ Creates a database connection """
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        # Optional performance boost for inserts:
        # conn.execute('PRAGMA synchronous = OFF;') # Don't wait for disk writes (faster, riskier)
        # conn.execute('PRAGMA journal_mode = MEMORY;') # Use in-memory journal (faster, riskier)
        # conn.execute('PRAGMA cache_size = 10000;') # Increase cache size (10MB example)
        # print(f"Connected to database: {db_file}")
        return conn
    except sqlite3.Error as e:
        print(f"Error connecting to database: {e}")
        return None

def setup_demo_table(conn):
    """ Creates a simple table for the batch insert demo, and clears data """
    create_items_table_sql = """
    CREATE TABLE IF NOT EXISTS large_items (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        value REAL
    );
    """
    try:
        cursor = conn.cursor()
        cursor.execute(create_items_table_sql)
        # Clear existing data for a clean batch insert demo
        cursor.execute("DELETE FROM large_items;")
        conn.commit()
        print("Demo table 'large_items' checked/created and cleared for batch insert demo.")
    except sqlite3.Error as e:
        print(f"Error setting up demo table: {e}")
        conn.rollback()

def perform_batch_insert_in_transaction(conn, data_list):
    """ Inserts a list of data using executemany within a transaction """
    sql = "INSERT INTO large_items (name, value) VALUES (?, ?);"
    print(f"\nAttempting to insert {len(data_list)} records in a batch transaction...")

    try:
        start_time = time.time()
        with conn: # Start transaction
            cursor = conn.cursor()
            cursor.executemany(sql, data_list)
        end_time = time.time()
        print(f"Batch insert successful.")
        print(f"Time taken: {end_time - start_time:.4f} seconds.")
        return cursor.rowcount # Total rows inserted
    except sqlite3.Error as e:
        print(f"\nError during batch insert transaction: {e}")
        print("Transaction automatically rolled back by the 'with conn:' context manager.")
        return 0
    except Exception as e:
        print(f"\nAn unexpected error occurred during batch insert: {e}")
        print("Transaction automatically rolled back by the 'with conn:' context manager.")
        return 0


def verify_count(conn):
    """ Counts records in the large_items table """
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM large_items;")
        count = cursor.fetchone()[0]
        print(f"\nTotal records in 'large_items' table: {count}")
        return count
    except sqlite3.Error as e:
        print(f"Error verifying count: {e}")
        return None


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

        # Generate a large list of dummy data
        num_records = 10000 # Adjust this number based on your system's performance
        dummy_data = [(f"Item_{i}", i * 0.5) for i in range(num_records)]
        print(f"Generated {num_records} dummy records for batch insert.")

        # Perform the batch insertion within a transaction
        inserted_count = perform_batch_insert_in_transaction(conn, dummy_data)

        # Verify the count
        verify_count(conn)

        # Optional: Demonstrate without transaction (will be much slower)
        # print("\n--- Demonstrating Batch Insert WITHOUT Transaction ---")
        # setup_demo_table(conn) # Clear table again
        # start_time = time.time()
        # cursor = conn.cursor()
        # for name, value in dummy_data:
        #     cursor.execute("INSERT INTO large_items (name, value) VALUES (?, ?);", (name, value))
        #     # Note: Each execute is implicitly a tiny transaction here if isolation_level is default
        #     # Or you'd call conn.commit() after each execute which is very slow.
        # conn.commit() # Commit all individual implicit transactions (or the final one)
        # end_time = time.time()
        # print(f"Insert without explicit batch transaction took: {end_time - start_time:.4f} seconds.")
        # verify_count(conn)


        conn.close()
        print(f"\nDatabase connection closed for {DATABASE_NAME}.")
    else:
        print("Failed to create database connection.")