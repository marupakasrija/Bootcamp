import sqlite3
import os
import csv

DATABASE_NAME = "store.db"

# --- Helper function to connect ---
def connect_db():
    """Establishes a connection to the SQLite database."""
    conn = None
    try:
        conn = sqlite3.connect(DATABASE_NAME)
        # conn.row_factory = sqlite3.Row # Optional: access columns by name
        return conn
    except sqlite3.Error as e:
        print(f"Database connection error: {e}")
        if conn:
            conn.close()
        return None

# --- Setting Up SQLite Database & Creating a Table ---
# Write a script to connect to store.db and create it if it doesn't exist.
# Use a SQL script to create this table in the store.db database.

def setup_database():
    """Connects to the database and creates the products table if it doesn't exist."""
    conn = connect_db()
    if conn:
        try:
            cursor = conn.cursor()
            # SQL script to create the table
            create_table_sql = """
            CREATE TABLE IF NOT EXISTS products (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                price REAL NOT NULL CHECK (price >= 0)
            );
            """
            cursor.execute(create_table_sql)
            conn.commit()
            print(f"Database '{DATABASE_NAME}' and table 'products' ensured.")
        except sqlite3.Error as e:
            print(f"Error setting up database: {e}")
            if conn:
                 conn.rollback() # Rollback in case of error during setup
        finally:
            if conn:
                conn.close()

# --- Inserting Data ---
# Write a function to insert a new product into the products table.
# The function should take name and price as parameters and insert them into the table.

def insert_product(name, price):
    """Inserts a new product into the products table."""
    conn = connect_db()
    if conn:
        try:
            cursor = conn.cursor()
            # Use parameterized queries to prevent SQL injection
            sql = "INSERT INTO products (name, price) VALUES (?, ?);"
            cursor.execute(sql, (name, price))
            conn.commit()
            print(f"Inserted product: {name} (Price: {price})")
        except sqlite3.Error as e:
            print(f"Error inserting product: {e}")
            if conn:
                 conn.rollback() # Rollback the insert on error
        finally:
            if conn:
                conn.close()

# --- Reading Data ---
# Implement a function to fetch and print all records from the products table.
# The function should query all records and print them out.

def get_all_products():
    """Fetches and returns all records from the products table."""
    conn = connect_db()
    products = []
    if conn:
        try:
            cursor = conn.cursor()
            sql = "SELECT id, name, price FROM products;"
            cursor.execute(sql)
            # fetchall() retrieves all rows from the query result
            products = cursor.fetchall()
            # If you set conn.row_factory = sqlite3.Row, you could access columns by name:
            # for row in products:
            #     print(f"ID: {row['id']}, Name: {row['name']}, Price: {row['price']}")

        except sqlite3.Error as e:
            print(f"Error fetching products: {e}")
        finally:
            if conn:
                conn.close()
    return products

def print_all_products():
    """Fetches and prints all records from the products table."""
    products = get_all_products()
    if products:
        print("\n--- All Products ---")
        for product in products:
            # Assuming default tuple format (id, name, price)
            print(f"ID: {product[0]}, Name: {product[1]}, Price: {product[2]}")
        print("--------------------")
    else:
        print("\nNo products found.")

# --- Updating Data ---
# Create a function to update the price of a product based on its id.
# This function should take id and new price as parameters and update the corresponding record.

def update_product_price(product_id, new_price):
    """Updates the price of a product by its ID."""
    conn = connect_db()
    if conn:
        try:
            cursor = conn.cursor()
            sql = "UPDATE products SET price = ? WHERE id = ?;"
            cursor.execute(sql, (new_price, product_id))
            conn.commit()
            # Check how many rows were affected
            if cursor.rowcount > 0:
                 print(f"Updated product ID {product_id} price to {new_price}")
            else:
                 print(f"No product found with ID {product_id} to update.")
        except sqlite3.Error as e:
            print(f"Error updating product: {e}")
            if conn:
                 conn.rollback()
        finally:
            if conn:
                conn.close()

# --- Deleting Data ---
# Write a function to delete a product from the table by its id.
# The function should take id as a parameter and remove the corresponding record.

def delete_product(product_id):
    """Deletes a product from the table by its ID."""
    conn = connect_db()
    if conn:
        try:
            cursor = conn.cursor()
            sql = "DELETE FROM products WHERE id = ?;"
            cursor.execute(sql, (product_id,)) # Note the comma to make it a tuple
            conn.commit()
            if cursor.rowcount > 0:
                print(f"Deleted product with ID {product_id}")
            else:
                print(f"No product found with ID {product_id} to delete.")
        except sqlite3.Error as e:
            print(f"Error deleting product: {e}")
            if conn:
                 conn.rollback()
        finally:
            if conn:
                conn.close()

# --- Exercise Execution ---
if __name__ == "__main__":
    # 1. Setup the database
    setup_database()

    # 2. Insert some data
    insert_product("Widget", 19.99)
    insert_product("Gadget", 29.50)
    insert_product("Thingamajig", 5.00)

    # 3. Read and print data
    print_all_products()

    # 4. Update data (assuming Widget was ID 1)
    # You might need to adjust the ID based on your inserts
    # A better approach would be to fetch the ID after insertion or query by name
    # Let's fetch the first product's ID to be safe for this example
    products_list = get_all_products()
    if products_list:
        first_product_id = products_list[0][0]
        update_product_price(first_product_id, 21.00)
        print_all_products() # See the updated price

    # 5. Delete data (assuming Gadget was ID 2)
    # Let's fetch the second product's ID
    products_list = get_all_products()
    if len(products_list) > 1:
         second_product_id = products_list[1][0]
         delete_product(second_product_id)
         print_all_products() # See the deleted product

    # Clean up the database file for re-runs (optional)
    # if os.path.exists(DATABASE_NAME):
    #     os.remove(DATABASE_NAME)
    #     print(f"\nRemoved database file {DATABASE_NAME}")