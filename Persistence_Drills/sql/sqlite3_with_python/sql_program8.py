import sqlite3
import os

DATABASE_NAME = "store_exceptions.db"

class ProductDBWithExceptions:
    def __init__(self, db_name=DATABASE_NAME):
        self.db_name = db_name
        self._ensure_table_exists()

    def _connect(self):
        """Establishes a connection to the database with exception handling."""
        conn = None
        try:
            conn = sqlite3.connect(self.db_name)
            # conn.row_factory = sqlite3.Row
            return conn
        except sqlite3.Error as e:
            # Log or print the specific database error
            print(f"Database connection error: {e}")
            # Re-raise the exception if you want calling code to handle it
            # raise
            if conn:
                conn.close()
            return None

    def _ensure_table_exists(self):
        """Creates the products table with exception handling."""
        conn = self._connect()
        if conn:
            try:
                cursor = conn.cursor()
                create_table_sql = """
                CREATE TABLE IF NOT EXISTS products (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL UNIQUE, -- Added UNIQUE constraint for testing errors
                    price REAL NOT NULL CHECK (price >= 0)
                );
                """
                cursor.execute(create_table_sql)
                conn.commit()
                print(f"Table 'products' ensured in '{self.db_name}'.")
            except sqlite3.Error as e:
                print(f"Error ensuring table exists: {e}")
                if conn:
                    conn.rollback()
            finally:
                if conn:
                    conn.close()

    def add_product(self, name, price):
        """Inserts a new product with exception handling."""
        conn = self._connect()
        if conn:
            try:
                cursor = conn.cursor()
                sql = "INSERT INTO products (name, price) VALUES (?, ?);"
                cursor.execute(sql, (name, price))
                conn.commit()
                print(f"Added product: {name}")
                return cursor.lastrowid
            # Catch specific SQLite errors
            except sqlite3.IntegrityError as e:
                 print(f"Error: Product with name '{name}' already exists (IntegrityError). {e}")
                 if conn: conn.rollback()
                 return None
            except sqlite3.OperationalError as e:
                print(f"Operational error adding product: {e}")
                if conn: conn.rollback()
                return None
            except sqlite3.Error as e:
                print(f"Generic SQLite error adding product: {e}")
                if conn: conn.rollback()
                return None
            except Exception as e:
                print(f"An unexpected error occurred adding product: {e}")
                if conn: conn.rollback() # Still rollback on unexpected errors
                return None
            finally:
                if conn:
                    conn.close()

    # ... (Implement get_all_products, update_product_price, delete_product with similar try-except blocks)
    # The get_all_products, update_product_price, delete_product methods from the previous example
    # already included basic sqlite3.Error handling.

    def print_products(self):
         """Helper method to print products."""
         # No specific error handling needed here beyond what get_all_products handles
         conn = self._connect()
         products = []
         if conn:
             try:
                 cursor = conn.cursor()
                 sql = "SELECT id, name, price FROM products;"
                 cursor.execute(sql)
                 products = cursor.fetchall()
                 if products:
                     print("\n--- Products in DB ---")
                     for product in products:
                         print(f"ID: {product[0]}, Name: {product[1]}, Price: {product[2]}")
                     print("----------------------")
                 else:
                     print("\nNo products in DB.")
             except sqlite3.Error as e:
                 print(f"Error fetching products for printing: {e}")
             finally:
                 if conn:
                     conn.close()


# --- Exercise Execution ---
if __name__ == "__main__":
    product_db = ProductDBWithExceptions()

    # Add products
    product_db.add_product("Desk", 150.00)
    product_db.add_product("Chair", 80.00)

    # Attempt to add a product with the same name (will trigger IntegrityError due to UNIQUE constraint)
    product_db.add_product("Desk", 160.00)

    # Attempt to add a product with invalid price (will trigger CHECK constraint error, often IntegrityError or OperationalError depending on SQLite version/context)
    product_db.add_product("Table", -10.00) # This might not be caught as a specific IntegrityError easily

    product_db.print_products()

    # Clean up (optional)
    # if os.path.exists(DATABASE_NAME):
    #     os.remove(DATABASE_NAME)
    #     print(f"\nRemoved database file {DATABASE_NAME}")