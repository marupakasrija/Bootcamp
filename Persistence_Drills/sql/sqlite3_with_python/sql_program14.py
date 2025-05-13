import sqlite3
import os
import csv

DATABASE_NAME = "store_export.db"
CSV_FILENAME = "products_export.csv"

class ProductDBWithExport:
    def __init__(self, db_name=DATABASE_NAME):
        self.db_name = db_name
        self._ensure_table_exists()
        self._add_initial_data() # Add some data

    def _connect(self):
        conn = None
        try:
            conn = sqlite3.connect(self.db_name)
            return conn
        except sqlite3.Error as e:
            print(f"Database connection error: {e}")
            if conn: conn.close()
            return None

    def _ensure_table_exists(self):
        conn = self._connect()
        if conn:
            try:
                cursor = conn.cursor()
                create_table_sql = """
                CREATE TABLE IF NOT EXISTS products (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL UNIQUE,
                    price REAL NOT NULL CHECK (price >= 0)
                );
                """
                cursor.execute(create_table_sql)
                conn.commit()
            except sqlite3.Error as e:
                print(f"Error ensuring table exists: {e}")
                if conn: conn.rollback()
            finally:
                if conn: conn.close()

    def _add_initial_data(self):
         conn = self._connect()
         if conn:
             try:
                 cursor = conn.cursor()
                 add_product_sql = "INSERT OR IGNORE INTO products (name, price) VALUES (?, ?);"
                 products_to_add = [
                     ("Pen", 1.50),
                     ("Notebook", 3.00),
                     ("Eraser", 0.75),
                 ]
                 cursor.executemany(add_product_sql, products_to_add)
                 conn.commit()
                 # print("Initial data added for export.")
             except sqlite3.Error as e:
                 print(f"Error adding initial data: {e}")
                 if conn: conn.rollback()
             finally:
                 if conn: conn.close()


    def export_products_to_csv(self, filename=CSV_FILENAME):
        """Exports all product data to a CSV file."""
        conn = self._connect()
        if conn:
            try:
                cursor = conn.cursor()
                sql = "SELECT id, name, price FROM products ORDER BY id;"
                cursor.execute(sql)

                # fetchall() gets all rows, fetchone() gets one, fetchmany(size) gets chunks
                # For potentially large datasets, consider fetching in chunks to save memory.
                # However, for typical CSV exports, fetchall is often fine.
                rows = cursor.fetchall()

                if not rows:
                     print("No data to export.")
                     return

                with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
                    # Use csv.writer
                    csv_writer = csv.writer(csvfile)

                    # Write header row (get column names from cursor.description)
                    # cursor.description is a list of tuples (name, type_code, ...)
                    header = [description[0] for description in cursor.description]
                    csv_writer.writerow(header)

                    # Write data rows
                    csv_writer.writerows(rows)

                print(f"Successfully exported data to {filename}")

            except sqlite3.Error as e:
                print(f"Error exporting data to CSV: {e}")
            except IOError as e:
                print(f"File writing error during CSV export: {e}")
            finally:
                if conn:
                    conn.close()

# --- Exercise Execution ---
if __name__ == "__main__":
    product_db = ProductDBWithExport()

    # Export the data
    product_db.export_products_to_csv()

    # Clean up (optional)
    # if os.path.exists(DATABASE_NAME):
    #     os.remove(DATABASE_NAME)
    #     print(f"\nRemoved database file {DATABASE_NAME}")
    # if os.path.exists(CSV_FILENAME):
    #     os.remove(CSV_FILENAME)
    #     print(f"Removed exported CSV file {CSV_FILENAME}")