import sqlite3
import os
import csv 

DATABASE_NAME = "store.db"
EXPORT_CSV_FILE = "products_export.csv"

def create_connection(db_file):
    """ Creates a database connection """
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        return conn
    except sqlite3.Error as e:
        print(f"Error connecting to database: {e}")
        return None

def export_products_to_csv(conn, csv_file):
    """ Fetches all products and exports them to a CSV file """
    sql = "SELECT id, name, price FROM products;" 
    try:
        cursor = conn.cursor()
        cursor.execute(sql)
        rows = cursor.fetchall()

        if not rows:
            print("No products found to export.")
            with open(csv_file, 'w', newline='', encoding='utf-8') as csvfile:
                 csv_writer = csv.writer(csvfile)
                 csv_writer.writerow(['id', 'name', 'price'])
            print(f"Created empty CSV file: {csv_file} with headers.")
            return

        
        headers = ['id', 'name', 'price'] 

        with open(csv_file, 'w', newline='', encoding='utf-8') as csvfile:
            csv_writer = csv.writer(csvfile)

            csv_writer.writerow(headers)

            csv_writer.writerows(rows)

        print(f"Successfully exported {len(rows)} products to {csv_file}")

    except sqlite3.Error as e:
        print(f"Database Error exporting data: {e}")
    except IOError as e:
        print(f"File Error writing CSV: {e}")
    except Exception as e:
        print(f"An unexpected error occurred during CSV export: {e}")


if __name__ == "__main__":
    script_dir = os.path.dirname(os.path.abspath(__file__))
    db_path = os.path.join(script_dir, DATABASE_NAME)
    csv_path = os.path.join(script_dir, EXPORT_CSV_FILE)

    if os.path.exists(csv_path):
        os.remove(csv_path)
        print(f"Removed existing CSV file: {csv_path}")

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
            exit() 

    conn = create_connection(db_path)

    if conn:
        print(f"Exporting data from {DATABASE_NAME}...")
        export_products_to_csv(conn, csv_path)
        conn.close()
        print(f"\nDatabase connection closed for {DATABASE_NAME}.")

    else:
        print("Failed to create database connection.")