import sqlite3
import os

DATABASE_NAME = "store_joins.db"

class ProductDBWithJoins:
    def __init__(self, db_name=DATABASE_NAME):
        self.db_name = db_name
        self._ensure_tables_exist()
        self._add_initial_data() # Add data to both tables

    def _connect(self):
        conn = None
        try:
            conn = sqlite3.connect(self.db_name)
            conn.row_factory = sqlite3.Row # Use Row factory to access columns by name
            return conn
        except sqlite3.Error as e:
            print(f"Database connection error: {e}")
            if conn: conn.close()
            return None

    def _ensure_tables_exist(self):
        """Ensures both products and categories tables exist."""
        conn = self._connect()
        if conn:
            try:
                cursor = conn.cursor()

                create_products_table_sql = """
                CREATE TABLE IF NOT EXISTS products (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL UNIQUE,
                    price REAL NOT NULL CHECK (price >= 0),
                    category_id INTEGER, -- Foreign key column
                    FOREIGN KEY (category_id) REFERENCES categories(id) -- Define foreign key constraint
                );
                """
                cursor.execute(create_products_table_sql)

                create_categories_table_sql = """
                CREATE TABLE IF NOT EXISTS categories (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL UNIQUE
                );
                """
                cursor.execute(create_categories_table_sql)

                conn.commit()
                print(f"Tables 'products' and 'categories' ensured in '{self.db_name}'.")
            except sqlite3.Error as e:
                print(f"Error ensuring tables exist: {e}")
                if conn: conn.rollback()
            finally:
                if conn: conn.close()

    def _add_initial_data(self):
         """Helper to add some data to categories and products."""
         conn = self._connect()
         if conn:
             try:
                 cursor = conn.cursor()

                 # Add categories (using INSERT OR IGNORE)
                 add_category_sql = "INSERT OR IGNORE INTO categories (name) VALUES (?);"
                 categories_to_add = [("Electronics",), ("Books",), ("Furniture",)]
                 cursor.executemany(add_category_sql, categories_to_add)

                 # Fetch category IDs to link products
                 cursor.execute("SELECT id, name FROM categories;")
                 categories = dict(cursor.fetchall()) # {name: id} mapping

                 # Add products (using INSERT OR IGNORE)
                 add_product_sql = "INSERT OR IGNORE INTO products (name, price, category_id) VALUES (?, ?, ?);"
                 products_to_add = [
                     ("Laptop", 1200.50, categories.get("Electronics")),
                     ("Python Programming", 45.00, categories.get("Books")),
                     ("Office Desk", 250.00, categories.get("Furniture")),
                     ("Smartphone", 800.00, categories.get("Electronics")),
                     ("SQL Guide", 30.00, categories.get("Books"))
                 ]
                 cursor.executemany(add_product_sql, products_to_add)

                 conn.commit()
                 # print("Initial data added for joins.")
             except sqlite3.Error as e:
                 print(f"Error adding initial data: {e}")
                 if conn: conn.rollback()
             finally:
                 if conn: conn.close()

    def get_products_with_categories(self):
        """Fetches products with their category names using a JOIN query."""
        conn = self._connect()
        products_with_categories = []
        if conn:
            try:
                cursor = conn.cursor()
                # Use a JOIN clause to combine rows from products and categories
                sql = """
                SELECT
                    p.id,
                    p.name AS product_name,
                    p.price,
                    c.name AS category_name
                FROM products AS p -- Alias 'products' table as 'p'
                LEFT JOIN categories AS c ON p.category_id = c.id; -- Join products with categories on the foreign key
                -- Using LEFT JOIN ensures products without a category are also included (category_name will be NULL)
                -- Use INNER JOIN if you only want products that *do* have a category.
                """
                cursor.execute(sql)
                products_with_categories = cursor.fetchall() # Returns a list of Row objects

            except sqlite3.Error as e:
                print(f"Error fetching products with categories: {e}")
            finally:
                if conn:
                    conn.close()
        return products_with_categories

    def print_products_with_categories(self):
         """Helper method to print products with category names."""
         products = self.get_products_with_categories()
         if products:
             print("\n--- Products with Categories ---")
             for product in products:
                 # Access columns by name due to row_factory = sqlite3.Row
                 print(f"ID: {product['id']}, Name: {product['product_name']}, "
                       f"Price: {product['price']}, Category: {product['category_name']}")
             print("------------------------------")
         else:
             print("\nNo products found.")


# --- Exercise Execution ---
if __name__ == "__main__":
    product_db = ProductDBWithJoins()

    # Fetch and print products with their categories
    product_db.print_products_with_categories()

    # Clean up (optional)
    # if os.path.exists(DATABASE_NAME):
    #     os.remove(DATABASE_NAME)
    #     print(f"\nRemoved database file {DATABASE_NAME}")