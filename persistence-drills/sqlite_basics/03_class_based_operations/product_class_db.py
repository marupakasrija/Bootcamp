import sqlite3
import os

DATABASE_NAME = "store.db"

class ProductDB:
    def __init__(self, db_file):
        self.db_file = db_file
        self._conn = None 

    def _get_connection(self):
        """ Gets or creates a database connection """
        if self._conn is None:
            try:
                self._conn = sqlite3.connect(self.db_file)
                print(f"Connected to database: {self.db_file}")
                self._create_table() 
            except sqlite3.Error as e:
                print(f"Database connection error: {e}")
                self._conn = None 
        return self._conn

    def close_connection(self):
        """ Closes the database connection """
        if self._conn:
            self._conn.close()
            self._conn = None 

    def _create_table(self):
        """ Creates the products table if it does not exist (internal helper) """
        create_products_table_sql = """
        CREATE TABLE IF NOT EXISTS products (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL UNIQUE, -- Added UNIQUE constraint for name validation example
            price REAL NOT NULL CHECK (price >= 0) -- Added CHECK constraint for price validation example
        );
        """
        conn = self._get_connection()
        if conn:
            try:
                cursor = conn.cursor()
                cursor.execute(create_products_table_sql)
                conn.commit()
            except sqlite3.Error as e:
                print(f"Error creating table: {e}")
                conn.rollback()

    def _validate_product_data(self, name, price):
        """ Basic data validation for name and price """
        if not isinstance(name, str) or not name.strip():
            raise ValueError("Product name must be a non-empty string.")
        if not isinstance(price, (int, float)) or price < 0:
            raise ValueError("Product price must be a non-negative number.")

    def add_product(self, name, price):
        """ Adds a new product to the database """
        conn = self._get_connection()
        if conn:
            try:
                self._validate_product_data(name, price) 

                sql = "INSERT INTO products (name, price) VALUES (?, ?);"
                cursor = conn.cursor()

                cursor.execute(sql, (name.strip(), price)) 
                product_id = cursor.lastrowid
                print(f"Successfully added product: '{name}' with ID {product_id}")
                return product_id
            except ValueError as ve:
                print(f"Validation Error: {ve}")
                return None
            except sqlite3.IntegrityError as ie:
                 print(f"Database Integrity Error (e.g., name already exists or price < 0): {ie}")
                 conn.rollback() 
                 return None
            except sqlite3.Error as e:
                print(f"Database Error adding product: {e}")
                conn.rollback() 
                return None
            except Exception as e:
                 print(f"An unexpected error occurred adding product: {e}")
                 conn.rollback() 
                 return None

    def get_all_products(self):
        """ Fetches all products from the database """
        conn = self._get_connection()
        if conn:
            try:
                sql = "SELECT id, name, price FROM products;"
                cursor = conn.cursor()
                cursor.execute(sql)
                rows = cursor.fetchall()
                return rows
            except sqlite3.Error as e:
                print(f"Database Error fetching products: {e}")
                return []
            except Exception as e:
                 print(f"An unexpected error occurred fetching products: {e}")
                 return []
        return []

    def search_products_by_name(self, name_fragment):
        """ Searches products by name fragment (case-insensitive) """
        conn = self._get_connection()
        if conn:
            try:
                sql = "SELECT id, name, price FROM products WHERE UPPER(name) LIKE ?;"
                search_term = f"%{name_fragment.upper()}%"
                cursor = conn.cursor()
                cursor.execute(sql, (search_term,))
                rows = cursor.fetchall()
                return rows
            except sqlite3.Error as e:
                print(f"Database Error searching products: {e}")
                return []
            except Exception as e:
                 print(f"An unexpected error occurred searching products: {e}")
                 return []
        return []

    def update_product_price(self, product_id, new_price):
        """ Updates the price of a product by ID """
        conn = self._get_connection()
        if conn:
             try:
                if not isinstance(new_price, (int, float)) or new_price < 0:
                   raise ValueError("New product price must be a non-negative number.")

                sql = "UPDATE products SET price = ? WHERE id = ?;"
                cursor = conn.cursor()
                cursor.execute(sql, (new_price, product_id))
                conn.commit()
                if cursor.rowcount > 0:
                    print(f"Successfully updated product ID {product_id} price to {new_price}")
                    return True
                else:
                    print(f"No product found with ID {product_id} to update.")
                    return False
             except ValueError as ve:
                print(f"Validation Error: {ve}")
                return False
             except sqlite3.Error as e:
                 print(f"Database Error updating product: {e}")
                 conn.rollback()
                 return False
             except Exception as e:
                 print(f"An unexpected error occurred updating product: {e}")
                 conn.rollback()
                 return False


    def delete_product(self, product_id):
        """ Deletes a product by ID """
        conn = self._get_connection()
        if conn:
            try:
                sql = "DELETE FROM products WHERE id = ?;"
                cursor = conn.cursor()
                cursor.execute(sql, (product_id,))
                conn.commit()
                if cursor.rowcount > 0:
                    print(f"Successfully deleted product with ID {product_id}")
                    return True
                else:
                    print(f"No product found with ID {product_id} to delete.")
                    return False
            except sqlite3.Error as e:
                print(f"Database Error deleting product: {e}")
                conn.rollback()
                return False
            except Exception as e:
                 print(f"An unexpected error occurred deleting product: {e}")
                 conn.rollback()
                 return False


if __name__ == "__main__":
    script_dir = os.path.dirname(os.path.abspath(__file__))
    db_path = os.path.join(script_dir, DATABASE_NAME)

    product_db = ProductDB(db_path)

    print("\n--- Adding Products ---")
    product_db.add_product("Laptop", 1200.50)
    product_db.add_product("Keyboard", 75.00)
    mouse_id = product_db.add_product("Mouse", 25.99)
    product_db.add_product("Monitor", 299.99)

    product_db.add_product("Laptop", 1500.00)

    product_db.add_product("Webcam", -10.00)

    product_db.add_product("", 50.00)


    print("\n--- All Products ---")
    all_products = product_db.get_all_products()
    if all_products:
         for p in all_products:
             print(f"ID: {p[0]}, Name: {p[1]}, Price: {p[2]}")
    else:
         print("No products found.")


    print("\n--- Updating Product ---")
    if mouse_id: 
        product_db.update_product_price(mouse_id, 22.50)
        product_db.update_product_price(999, 100) 

    print("\n--- Deleting Product ---")
    keyboard_products = product_db.search_products_by_name("Keyboard")
    if keyboard_products:
        keyboard_id_to_delete = keyboard_products[0][0]
        product_db.delete_product(keyboard_id_to_delete)
    product_db.delete_product(9999) 


    print("\n--- Remaining Products ---")
    all_products_after_crud = product_db.get_all_products()
    if all_products_after_crud:
         for p in all_products_after_crud:
             print(f"ID: {p[0]}, Name: {p[1]}, Price: {p[2]}")
    else:
         print("No products found.")


    print("\n--- Searching Products ---")
    search_results = product_db.search_products_by_name("lap")
    print("Search results for 'lap':")
    if search_results:
        for p in search_results:
            print(f"ID: {p[0]}, Name: {p[1]}, Price: {p[2]}")
    else:
        print("No products found matching 'lap'.")

    search_results_mouse = product_db.search_products_by_name("Mouse")
    print("Search results for 'Mouse' (after deletion):")
    if search_results_mouse:
         for p in search_results_mouse:
             print(f"ID: {p[0]}, Name: {p[1]}, Price: {p[2]}")
    else:
         print("No products found matching 'Mouse'.")


    product_db.close_connection()
    print("\nDatabase connection closed.")