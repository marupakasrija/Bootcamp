import sqlite3
import os

DATABASE_NAME = "store_validation.db"

class ProductDBWithValidation:
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

    def add_product(self, name, price):
        """Inserts a new product with data validation."""
        # --- Validation Logic ---
        if not isinstance(name, str) or not name.strip():
            print("Validation Error: Product name must be a non-empty string.")
            return None
        if not isinstance(price, (int, float)) or price < 0:
            print("Validation Error: Product price must be a non-negative number.")
            return None
        # --- End Validation Logic ---

        conn = self._connect()
        if conn:
            try:
                cursor = conn.cursor()
                sql = "INSERT INTO products (name, price) VALUES (?, ?);"
                cursor.execute(sql, (name.strip(), price)) # Strip whitespace from name
                conn.commit()
                print(f"Added product: {name.strip()}")
                return cursor.lastrowid
            except sqlite3.IntegrityError as e:
                 print(f"Error: Product with name '{name.strip()}' already exists. {e}")
                 if conn: conn.rollback()
                 return None
            except sqlite3.Error as e:
                print(f"SQLite error adding product: {e}")
                if conn: conn.rollback()
                return None
            finally:
                if conn:
                    conn.close()

    def update_product_price(self, product_id, new_price):
        """Updates the price of a product with data validation."""
        # --- Validation Logic ---
        if not isinstance(product_id, int) or product_id <= 0:
             print("Validation Error: Product ID must be a positive integer.")
             return False
        if not isinstance(new_price, (int, float)) or new_price < 0:
            print("Validation Error: New price must be a non-negative number.")
            return False
        # --- End Validation Logic ---

        conn = self._connect()
        if conn:
            try:
                cursor = conn.cursor()
                sql = "UPDATE products SET price = ? WHERE id = ?;"
                cursor.execute(sql, (new_price, product_id))
                conn.commit()
                if cursor.rowcount > 0:
                    print(f"Updated product ID {product_id}")
                    return True
                else:
                    print(f"Product ID {product_id} not found for update.")
                    return False
            except sqlite3.Error as e:
                print(f"Error updating product: {e}")
                if conn:
                    conn.rollback()
                return False
            finally:
                if conn:
                    conn.close()

    # ... (Include other methods like get_all_products, delete_product, print_products)
    def get_all_products(self):
        """Fetches all products."""
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
         """Helper method to print products."""
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
    product_db = ProductDBWithValidation()

    print("Attempting valid insertions:")
    product_id_A = product_db.add_product("Laptop", 1200.50)
    product_id_B = product_db.add_product("Mousepad", 10.00)
    product_db.print_products()

    print("\nAttempting invalid insertions:")
    product_db.add_product("", 50.00)         # Empty name
    product_db.add_product("Desk", -20.00)    # Negative price
    product_db.add_product("Chair", "invalid_price") # Non-numeric price
    product_db.add_product(123, 70.00)        # Non-string name

    product_db.print_products() # Should only show Laptop and Mousepad

    print("\nAttempting valid update:")
    if product_id_A is not None:
         product_db.update_product_price(product_id_A, 1150.00)
    product_db.print_products()

    print("\nAttempting invalid updates:")
    product_db.update_product_price(-1, 100.00)    # Invalid ID
    if product_id_B is not None:
        product_db.update_product_price(product_id_B, -5.00) # Negative price
        product_db.update_product_price(product_id_B, "invalid_price") # Non-numeric price

    product_db.print_products() # Should not show changes from invalid updates

    # Clean up (optional)
    # if os.path.exists(DATABASE_NAME):
    #     os.remove(DATABASE_NAME)
    #     print(f"\nRemoved database file {DATABASE_NAME}")