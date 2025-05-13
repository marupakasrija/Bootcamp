import sqlite3
import os

DATABASE_NAME = "store_transactions.db"

class ProductDBWithTransactions:
    def __init__(self, db_name=DATABASE_NAME):
        self.db_name = db_name
        self._ensure_table_exists()

    def _connect(self):
        conn = None
        try:
            # By default, sqlite3 creates a transaction implicitly.
            # You can control this with the 'isolation_level' parameter.
            # None means autocommit mode (each statement is a transaction).
            # 'DEFERRED', 'IMMEDIATE', 'EXCLUSIVE' start transactions.
            # We'll stick to the default (autocommit) for simple ops,
            # but show explicit begin/commit/rollback where needed later.
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

    def add_product(self, name, price):
        """Inserts a new product (example of explicit transaction, though autocommit works)."""
        if not isinstance(name, str) or not name.strip():
            print("Validation Error: Product name must be a non-empty string.")
            return None
        if not isinstance(price, (int, float)) or price < 0:
            print("Validation Error: Product price must be a non-negative number.")
            return None

        conn = self._connect()
        if conn:
            try:
                # Explicitly begin a transaction (useful for multi-statement operations)
                conn.execute("BEGIN;") # Or simply omit, as it's default behavior for first statement

                cursor = conn.cursor()
                sql = "INSERT INTO products (name, price) VALUES (?, ?);"
                cursor.execute(sql, (name.strip(), price))

                conn.commit() # Commit the transaction if successful
                print(f"Added product: {name.strip()}")
                return cursor.lastrowid
            except sqlite3.Error as e:
                print(f"Error adding product: {e}")
                if conn:
                    conn.rollback() # Rollback the transaction on error
                return None
            finally:
                if conn:
                    conn.close()

    # ... (Include other methods - get_all_products, update_product_price, delete_product)
    # For simple single operations, autocommit is usually sufficient in SQLite.
    # Transactions become critical for operations affecting multiple rows or tables.

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
    product_db = ProductDBWithTransactions()

    # Demonstrate adding a product
    product_db.add_product("Headphones", 99.99)
    product_db.add_product("Webcam", 55.00)
    product_db.print_products()

    # Clean up (optional)
    # if os.path.exists(DATABASE_NAME):
    #     os.remove(DATABASE_NAME)
    #     print(f"\nRemoved database file {DATABASE_NAME}")