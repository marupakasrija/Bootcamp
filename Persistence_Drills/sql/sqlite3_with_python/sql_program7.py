import sqlite3
import os

DATABASE_NAME = "store_oop.db" # Use a different database name

class ProductDB:
    def __init__(self, db_name=DATABASE_NAME):
        self.db_name = db_name
        self._ensure_table_exists()

    def _connect(self):
        """Establishes a connection to the database."""
        conn = None
        try:
            conn = sqlite3.connect(self.db_name)
            # conn.row_factory = sqlite3.Row # Optional: access columns by name
            return conn
        except sqlite3.Error as e:
            print(f"Database connection error: {e}")
            if conn:
                conn.close()
            return None

    def _ensure_table_exists(self):
        """Creates the products table if it doesn't exist."""
        conn = self._connect()
        if conn:
            try:
                cursor = conn.cursor()
                create_table_sql = """
                CREATE TABLE IF NOT EXISTS products (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL,
                    price REAL NOT NULL CHECK (price >= 0)
                );
                """
                cursor.execute(create_table_sql)
                conn.commit()
                # print(f"Table 'products' ensured in '{self.db_name}'.")
            except sqlite3.Error as e:
                print(f"Error ensuring table exists: {e}")
                if conn:
                    conn.rollback()
            finally:
                if conn:
                    conn.close()

    def add_product(self, name, price):
        """Inserts a new product."""
        conn = self._connect()
        if conn:
            try:
                cursor = conn.cursor()
                sql = "INSERT INTO products (name, price) VALUES (?, ?);"
                cursor.execute(sql, (name, price))
                conn.commit()
                print(f"Added product: {name}")
                return cursor.lastrowid # Return the ID of the newly inserted row
            except sqlite3.Error as e:
                print(f"Error adding product: {e}")
                if conn:
                    conn.rollback()
                return None
            finally:
                if conn:
                    conn.close()

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

    def update_product_price(self, product_id, new_price):
        """Updates the price of a product by ID."""
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

    def delete_product(self, product_id):
        """Deletes a product by ID."""
        conn = self._connect()
        if conn:
            try:
                cursor = conn.cursor()
                sql = "DELETE FROM products WHERE id = ?;"
                cursor.execute(sql, (product_id,))
                conn.commit()
                if cursor.rowcount > 0:
                    print(f"Deleted product with ID {product_id}")
                    return True
                else:
                    print(f"Product ID {product_id} not found for deletion.")
                    return False
            except sqlite3.Error as e:
                print(f"Error deleting product: {e}")
                if conn:
                    conn.rollback()
                return False
            finally:
                if conn:
                    conn.close()

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
    # Instantiate the class (this will also ensure the table exists)
    product_db = ProductDB()

    # Add products
    product_id_1 = product_db.add_product("Keyboard", 75.00)
    product_id_2 = product_db.add_product("Mouse", 25.99)
    product_id_3 = product_db.add_product("Monitor", 199.50)

    # List products
    product_db.print_products()

    # Update a product
    if product_id_1 is not None:
        product_db.update_product_price(product_id_1, 70.00)
    product_db.print_products()

    # Delete a product
    if product_id_2 is not None:
        product_db.delete_product(product_id_2)
    product_db.print_products()

    # Clean up the database file (optional)
    # if os.path.exists(DATABASE_NAME):
    #     os.remove(DATABASE_NAME)
    #     print(f"\nRemoved database file {DATABASE_NAME}")