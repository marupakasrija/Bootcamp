# 06_aggregation_queries/aggregation_queries.py
import sqlite3
import os

# Define the database file name
DATABASE_NAME = "store.db"

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

def setup_products_table(conn):
    """ Creates the products table if it does not exist """
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
        conn.commit()
        print("Products table checked/created.")
    except sqlite3.Error as e:
        print(f"Error setting up products table: {e}")
        conn.rollback()


def add_product(conn, name, price):
    """ Inserts a product, ignoring if name exists """
    sql = "INSERT OR IGNORE INTO products (name, price) VALUES (?, ?);"
    try:
        cursor = conn.cursor()
        cursor.execute(sql, (name, price))
        conn.commit()
        if cursor.rowcount > 0:
            # print(f"Added product: {name}")
            return cursor.lastrowid
        # else:
            # print(f"Product '{name}' already exists, skipped insertion.")
        return None # Return None if ignored
    except sqlite3.Error as e:
        print(f"Error adding product '{name}': {e}")
        conn.rollback()
        return None


def calculate_total_value(conn):
    """ Calculates the sum of prices of all products """
    sql = "SELECT SUM(price) FROM products;"
    try:
        cursor = conn.cursor()
        cursor.execute(sql)
        total_value = cursor.fetchone()[0]
        # SUM returns None if the table is empty, handle this
        return total_value if total_value is not None else 0
    except sqlite3.Error as e:
        print(f"Error calculating total value: {e}")
        return None

def count_products(conn):
    """ Counts the total number of products """
    sql = "SELECT COUNT(*) FROM products;"
    try:
        cursor = conn.cursor()
        cursor.execute(sql)
        count = cursor.fetchone()[0]
        return count
    except sqlite3.Error as e:
        print(f"Error counting products: {e}")
        return None

def calculate_average_price(conn):
    """ Calculates the average price of products """
    sql = "SELECT AVG(price) FROM products;"
    try:
        cursor = conn.cursor()
        cursor.execute(sql)
        average_price = cursor.fetchone()[0]
         # AVG returns None if the table is empty
        return average_price if average_price is not None else 0.0
    except sqlite3.Error as e:
        print(f"Error calculating average price: {e}")
        return None

# --- Main Execution ---
if __name__ == "__main__":
    script_dir = os.path.dirname(os.path.abspath(__file__))
    db_path = os.path.join(script_dir, DATABASE_NAME)

    # Clean up the database file for a fresh start for THIS script's demo
    # Note: If you want to run this after 02 or 03 and use their data, comment this out.
    # Ensure the products table structure is compatible if using data from other scripts.
    if os.path.exists(db_path):
         os.remove(db_path)
         print(f"Removed existing database: {db_path}")


    conn = create_connection(db_path)

    if conn:
        setup_products_table(conn)

        # Add some sample data for aggregation
        print("--- Adding Sample Products for Aggregation ---")
        add_product(conn, "Widget A", 10.50)
        add_product(conn, "Gadget B", 22.00)
        add_product(conn, "Thing C", 5.75)
        add_product(conn, "Widget D", 10.50) # Same price as A
        add_product(conn, "Gadget E", 22.00) # Same price as B
        add_product(conn, "Item F", 1.99)

        # Run aggregation queries
        print("\n--- Aggregation Results ---")
        total = calculate_total_value(conn)
        count = count_products(conn)
        average = calculate_average_price(conn)

        print(f"Total value of all products: {total:.2f}" if total is not None else "Could not calculate total value.")
        print(f"Total number of products: {count}" if count is not None else "Could not count products.")
        print(f"Average product price: {average:.2f}" if average is not None else "Could not calculate average price.")


        # Close the connection
        conn.close()
        print(f"\nDatabase connection closed for {DATABASE_NAME}.")
    else:
        print("Failed to create database connection.")