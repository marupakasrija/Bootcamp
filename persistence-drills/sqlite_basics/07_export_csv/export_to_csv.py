# 07_export_csv/export_to_csv.py
import sqlite3
import os
import csv # Python's built-in CSV module

# Define the database file name
DATABASE_NAME = "store.db"
EXPORT_CSV_FILE = "products_export.csv"

def create_connection(db_file):
    """ Creates a database connection """
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        # Optional: Set row_factory to access columns by name, useful for CSV headers
        # conn.row_factory = sqlite3.Row
        # print(f"Connected to database: {db_file}")
        return conn
    except sqlite3.Error as e:
        print(f"Error connecting to database: {e}")
        return None

def export_products_to_csv(conn, csv_file):
    """ Fetches all products and exports them to a CSV file """
    sql = "SELECT id, name, price FROM products;" # Select data you want to export
    try:
        cursor = conn.cursor()
        cursor.execute(sql)
        rows = cursor.fetchall()

        if not rows:
            print("No products found to export.")
            # Optionally create an empty CSV or skip creation
            with open(csv_file, 'w', newline='', encoding='utf-8') as csvfile:
                 csv_writer = csv.writer(csvfile)
                 # Write headers even if no data
                 csv_writer.writerow(['id', 'name', 'price'])
            print(f"Created empty CSV file: {csv_file} with headers.")
            return

        # Get column names from cursor description if row_factory is not used
        # If using row_factory = sqlite3.Row, you can get headers from rows[0].keys()
        # headers = [description[0] for description in cursor.description]
        headers = ['id', 'name', 'price'] # Manually defined headers to match the query

        with open(csv_file, 'w', newline='', encoding='utf-8') as csvfile:
            csv_writer = csv.writer(csvfile)

            # Write header row
            csv_writer.writerow(headers)

            # Write data rows
            csv_writer.writerows(rows)

        print(f"Successfully exported {len(rows)} products to {csv_file}")

    except sqlite3.Error as e:
        print(f"Database Error exporting data: {e}")
    except IOError as e:
        print(f"File Error writing CSV: {e}")
    except Exception as e:
        print(f"An unexpected error occurred during CSV export: {e}")


# --- Main Execution ---
if __name__ == "__main__":
    script_dir = os.path.dirname(os.path.abspath(__file__))
    db_path = os.path.join(script_dir, DATABASE_NAME)
    csv_path = os.path.join(script_dir, EXPORT_CSV_FILE)

    # Clean up previous CSV export if it exists
    if os.path.exists(csv_path):
        os.remove(csv_path)
        print(f"Removed existing CSV file: {csv_path}")

    # --- Create a dummy database with data if it doesn't exist ---
    # This script depends on data existing. If running this standalone,
    # you need to populate store.db first.
    # For demonstration, let's create a simple store.db if not found.
    if not os.path.exists(db_path):
        print(f"Database '{DATABASE_NAME}' not found. Creating with sample data for export demo.")
        dummy_conn = create_connection(db_path)
        if dummy_conn:
             cursor = dummy_conn.cursor()
             cursor.execute("""
             CREATE TABLE products (
                 id INTEGER PRIMARY KEY AUTOINCREMENT,
                 name TEXT NOT NULL UNIQUE,
                 price REAL NOT NULL CHECK (price >= 0)
             );""")
             cursor.execute("INSERT INTO products (name, price) VALUES ('Dummy Product 1', 10.00);")
             cursor.execute("INSERT INTO products (name, price) VALUES ('Dummy Product 2', 20.00);")
             dummy_conn.commit()
             dummy_conn.close()
             print("Dummy data created.")
        else:
            print("Could not create dummy database. Cannot proceed with export.")
            exit() # Exit if we can't even create the dummy db

    # --- Proceed with Export ---
    conn = create_connection(db_path)

    if conn:
        print(f"Exporting data from {DATABASE_NAME}...")
        export_products_to_csv(conn, csv_path)
        conn.close()
        print(f"\nDatabase connection closed for {DATABASE_NAME}.")

        # Optional: Print CSV content to verify
        # try:
        #     with open(csv_path, 'r', encoding='utf-8') as f:
        #         print("\n--- Content of exported CSV ---")
        #         print(f.read())
        #         print("-----------------------------")
        # except FileNotFoundError:
        #      print("CSV file not found after export attempt.")


    else:
        print("Failed to create database connection.")