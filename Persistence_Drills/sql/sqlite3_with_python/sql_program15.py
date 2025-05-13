import sqlite3
import os

DATABASE_NAME = "store_batch_insert.db"

class ProductDBWithBatchInsert:
    def __init__(self, db_name=DATABASE_NAME):
        self.db_name = db_name
        self._ensure_table_exists()

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

    def batch_add_products(self, product_list):
        """Inserts multiple products using a single transaction."""
        # Validate input: product_list should be a list of tuples or lists
        if not isinstance(product_list, list):
            print("Validation Error: Input must be a list of products.")
            return False

        # Basic validation for each item in the list (can be expanded)
        for item in product_list:
            if not isinstance(item, (list, tuple)) or len(item) != 2:
                 print(f"Validation Error: Each item in the list must be a tuple/list of (name, price): {item}")
                 return False
            name, price = item
            if not isinstance(name, str) or not name.strip():
                print(f"Validation Error: Product name must be a non-empty string: {name}")
                return False
            if not isinstance(price, (int, float)) or price < 0:
                 print(f"Validation Error: Product price must be a non-negative number: {price}")
                 return False


        conn = self._connect()
        if conn:
            try:
                # Explicitly begin a transaction for the batch operation
                # SQLite typically handles transactions well with executemany and default isolation
                # but explicitly beginning can sometimes make intent clearer or be necessary for
                # specific isolation levels or error handling patterns.
                # conn.execute("BEGIN;")

                cursor = conn.cursor()
                sql = "INSERT INTO products (name, price) VALUES (?, ?);"
                # executemany is designed for batch operations
                cursor.executemany(sql, product_list)

                conn.commit() # Commit all inserts if executemany succeeds
                print(f"Successfully added {len(product_list)} products in batch.")
                return True
            except sqlite3.IntegrityError as e:
                 print(f"Error during batch insert (IntegrityError): At least one product name already exists. {e}")
                 if conn: conn.rollback() # Rollback the entire batch on any integrity error
                 return False
            except sqlite3.Error as e:
                print(f"SQLite error during batch insert: {e}")
                if conn: conn.rollback() # Rollback the entire batch on any SQLite error
                return False
            finally:
                if conn:
                    conn.close()
        return False # Return False if connection failed

    # ... (Include print_products method)
    def get_all_products(self):
        conn = self._connect()
        products = []
        if conn:
            try:
                cursor = conn.cursor()
                sql = "SELECT id, name, price FROM products;"
                cursor.execute(sql)
                products = cursor.fetchall()
            except sqlite3.Error as e:
                print(f"Error fetching products: {e}")
            finally:
                if conn:
                    conn.close()
        return products

    def print_products(self):
         products = self.get_all_products()
         if products:
             print("\n--- Products in DB ---")
             for product in products:
                 print(f"ID: {product[0]}, Name: {product[1]}, Price: {product[2]}")
             print("----------------------")
         else:
             print("\nNo products in DB.")


# --- Exercise Execution ---
if __name__ == "__main__":
    product_db = ProductDBWithBatchInsert()

    products_to_add = [
        ("Laptop Case", 35.00),
        ("External Hard Drive", 90.00),
        ("USB Hub", 15.00),
        ("Monitor Stand", 45.00),
    ]

    # Perform batch insertion
    success = product_db.batch_add_products(products_to_add)

    if success:
        product_db.print_products()

    # Attempt batch insertion with a duplicate name to trigger rollback
    print("\nAttempting batch insert with a duplicate:")
    products_with_duplicate = [
         ("Desk Lamp", 25.00),
         ("Laptop Case", 30.00), # Duplicate name
         ("Speakers", 120.00),
    ]
    success_duplicate = product_db.batch_add_products(products_with_duplicate)

    if not success_duplicate:
         print("Batch insert with duplicate failed as expected. Checking product list...")
    product_db.print_products() # Should NOT include Desk Lamp or Speakers if rollback worked

    # Attempt batch insertion with invalid data
    print("\nAttempting batch insert with invalid data:")
    products_with_invalid = [
        ("Webcam Cover", 5.00),
        ("Adapter", -10.00), # Invalid price
        ("Cleaning Kit", 12.00),
    ]
    success_invalid = product_db.batch_add_products(products_with_invalid)

    if not success_invalid:
         print("Batch insert with invalid data failed as expected. Checking product list...")
    product_db.print_products() # Should NOT include Webcam Cover or Cleaning Kit if rollback worked

    # Clean up (optional)
    # if os.path.exists(DATABASE_NAME):
    #     os.remove(DATABASE_NAME)
    #     print(f"\nRemoved database file {DATABASE_NAME}")