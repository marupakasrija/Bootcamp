# 08_batch_operations/batch_insert.py
import sqlite3
import os
import time

# Define the database file name
DATABASE_NAME = "store.db"

def create_connection(db_file):
    """ Creates a database connection """
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        # Optional: Increase the cache size for potentially faster imports
        # conn.execute('PRAGMA cache_size = 20000;') # Set cache size to 20MB (example)
        # print(f"Connected to database: {db_file}")
        return conn
    except sqlite3.Error as e:
        print(f"Error connecting to database: {e}")
        return None

def setup_products_table(conn):
    """ Creates the products table if it does not exist, and clears existing data """
    create_products_table_sql = """
    CREATE TABLE IF NOT EXISTS products (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL UNIQUE,
        price REAL NOT NULL CHECK (price >= 0)
    );
    """
    try:
        cursor = conn.cursor()
        cursor.execute(create_products_table_sql)
        # Clear existing data for a clean batch insert demo
        cursor.execute("DELETE FROM products;")
        conn.commit()
        print("Products table checked/created and cleared for batch insert demo.")
    except sqlite3.Error as e:
        print(f"Error setting up products table: {e}")
        conn.rollback()

def insert_many_products(conn, products_list):
    """ Inserts multiple products using executemany """
    sql = "INSERT INTO products (name, price) VALUES (?, ?);"
    try:
        cursor = conn.cursor()
        start_time = time.time()

        # Using the connection as a context manager provides a transaction
        with conn:
            # executemany is significantly faster for multiple inserts
            cursor.executemany(sql, products_list)

        end_time = time.time()
        print(f"Successfully inserted {len(products_list)} products in {end_time - start_time:.4f} seconds (batch).")
        return cursor.rowcount # rowcount after executemany is total rows affected

    except sqlite3.Error as e:
        print(f"Error during batch insert: {e}")
        # Rollback is automatic with 'with conn:' on exception
        return 0
    except Exception as e:
        print(f"An unexpected error occurred during batch insert: {e}")
        return 0


# --- Main Execution ---
if __name__ == "__main__":
    script_dir = os.path.dirname(os.path.abspath(__file__))
    db_path = os.path.join(script_dir, DATABASE_NAME)

    # Clean up the database file for a fresh start for THIS script's demo
    # if os.path.exists(db_path):
    #      os.remove(db_path)
    #      print(f"Removed existing database: {db_path}")

    conn = create_connection(db_path)

    if conn:
        setup_products_table(conn)

        # Prepare data for batch insertion
        num_products_to_insert = 1000
        products_data = [(f"Batch Product {i}", 10.0 + i * 0.1) for i in range(num_products_to_insert)]
        print(f"\nPreparing to insert {num_products_to_insert} products...")

        # Perform batch insertion
        inserted_count = insert_many_products(conn, products_data)
        print(f"Total rows inserted: {inserted_count}")

        # Verify the count
        try:
            cursor = conn.cursor()
            cursor.execute("SELECT COUNT(*) FROM products;")
            total_rows_in_db = cursor.fetchone()[0]
            print(f"Total rows currently in the database: {total_rows_in_db}")
        except sqlite3.Error as e:
            print(f"Error verifying row count: {e}")


        # Close the connection
        conn.close()
        print(f"\nDatabase connection closed for {DATABASE_NAME}.")
    else:
        print("Failed to create database connection.")