import sqlite3
import os

DATABASE_NAME = "store_search.db"

class ProductDBWithSearch:
    def __init__(self, db_name=DATABASE_NAME):
        self.db_name = db_name
        self._ensure_table_exists()
        self._add_initial_data() # Add some data for searching

    def _connect(self):
        conn = None
        try:
            conn = sqlite3.connect(self.db_name)
            # conn.row_factory = sqlite3.Row
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
         """Helper to add some data for testing search."""
         conn = self._connect()
         if conn:
             try:
                 cursor = conn.cursor()
                 # Use INSERT OR IGNORE to avoid adding duplicates if run multiple times
                 sql = "INSERT OR IGNORE INTO products (name, price) VALUES (?, ?);"
                 products_to_add = [
                     ("Apple iPhone 13", 699.99),
                     ("Samsung Galaxy S22", 799.00),
                     ("Google Pixel 6", 599.50),
                     ("Apple iPad Air", 550.00),
                     ("Microsoft Surface", 999.99)
                 ]
                 cursor.executemany(sql, products_to_add) # Use executemany for multiple inserts
                 conn.commit()
                 # print("Initial data added for search.")
             except sqlite3.Error as e:
                 print(f"Error adding initial data: {e}")
                 if conn: conn.rollback()
             finally:
                 if conn: conn.close()


    def search_products_by_name(self, name_fragment):
        """Searches for products whose name contains the given fragment."""
        conn = self._connect()
        matching_products = []
        if conn:
            try:
                cursor = conn.cursor()
                # Use LIKE with '%' wildcards for partial matching (case-insensitive in SQLite by default)
                sql = "SELECT id, name, price FROM products WHERE name LIKE ?;"
                # Add '%' around the fragment for "contains" search
                search_term = f"%{name_fragment}%"
                cursor.execute(sql, (search_term,))
                matching_products = cursor.fetchall()

            except sqlite3.Error as e:
                print(f"Error searching products: {e}")
            finally:
                if conn:
                    conn.close()
        return matching_products

    def print_products(self, products):
         """Helper method to print a list of products."""
         if products:
             print("\n--- Found Products ---")
             for product in products:
                 print(f"ID: {product[0]}, Name: {product[1]}, Price: {product[2]}")
             print("--------------------")
         else:
             print("\nNo products found.")

# --- Exercise Execution ---
if __name__ == "__main__":
    product_db = ProductDBWithSearch()

    # Search for products containing "Apple"
    apple_products = product_db.search_products_by_name("Apple")
    print("Searching for 'Apple':")
    product_db.print_products(apple_products)

    # Search for products containing "Galaxy"
    galaxy_products = product_db.search_products_by_name("Galaxy")
    print("\nSearching for 'Galaxy':")
    product_db.print_products(galaxy_products)

    # Search for products containing "tablet" (should find none with current data)
    tablet_products = product_db.search_products_by_name("tablet")
    print("\nSearching for 'tablet':")
    product_db.print_products(tablet_products)

    # Clean up (optional)
    # if os.path.exists(DATABASE_NAME):
    #     os.remove(DATABASE_NAME)
    #     print(f"\nRemoved database file {DATABASE_NAME}")