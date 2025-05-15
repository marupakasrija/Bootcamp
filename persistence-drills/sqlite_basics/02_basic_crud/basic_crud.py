# 02_basic_crud/basic_crud.py
import sqlite3
import os

# Define the database file name
DATABASE_NAME = "store.db"

def create_connection(db_file):
    """ Creates a database connection to the SQLite database specified by db_file """
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        print(f"Connected to database: {db_file} (SQLite version {sqlite3.version})")
        return conn
    except sqlite3.Error as e:
        print(f"Error connecting to database: {e}")
        if conn:
            conn.close()
        return None

def create_table(conn):
    """ Creates the products table if it does not exist """
    create_products_table_sql = """
    CREATE TABLE IF NOT EXISTS products (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        price REAL NOT NULL
    );
    """
    try:
        cursor = conn.cursor()
        cursor.execute(create_products_table_sql)
        print("Products table checked/created successfully.")
        conn.commit() # Commit the table creation
    except sqlite3.Error as e:
        print(f"Error creating table: {e}")
        conn.rollback()

def insert_product(conn, name, price):
    """ Inserts a new product into the products table """
    sql = """
    INSERT INTO products (name, price) VALUES (?, ?);
    """
    try:
        cursor = conn.cursor()
        cursor.execute(sql, (name, price)) # Use parameterized query to prevent SQL injection
        conn.commit()
        product_id = cursor.lastrowid
        print(f"Inserted product: {name} with ID {product_id}")
        return product_id
    except sqlite3.Error as e:
        print(f"Error inserting product: {e}")
        conn.rollback()
        return None

def select_all_products(conn):
    """ Fetches and prints all records from the products table """
    sql = """
    SELECT id, name, price FROM products;
    """
    try:
        cursor = conn.cursor()
        cursor.execute(sql)
        rows = cursor.fetchall()
        print("\n--- All Products ---")
        if not rows:
            print("No products found.")
        else:
            for row in rows:
                print(f"ID: {row[0]}, Name: {row[1]}, Price: {row[2]}")
        print("--------------------")
        return rows
    except sqlite3.Error as e:
        print(f"Error fetching products: {e}")
        return []

def update_product_price(conn, product_id, new_price):
    """ Updates the price of a product based on its ID """
    sql = """
    UPDATE products SET price = ? WHERE id = ?;
    """
    try:
        cursor = conn.cursor()
        cursor.execute(sql, (new_price, product_id))
        conn.commit()
        if cursor.rowcount > 0:
            print(f"Updated product with ID {product_id}: new price {new_price}")
            return True
        else:
            print(f"No product found with ID {product_id} to update.")
            return False
    except sqlite3.Error as e:
        print(f"Error updating product: {e}")
        conn.rollback()
        return False

def delete_product(conn, product_id):
    """ Deletes a product from the table by its ID """
    sql = """
    DELETE FROM products WHERE id = ?;
    """
    try:
        cursor = conn.cursor()
        cursor.execute(sql, (product_id,)) # Tuple with comma for single item
        conn.commit()
        if cursor.rowcount > 0:
            print(f"Deleted product with ID {product_id}")
            return True
        else:
            print(f"No product found with ID {product_id} to delete.")
            return False
    except sqlite3.Error as e:
        print(f"Error deleting product: {e}")
        conn.rollback()
        return False


# --- Main Execution ---
if __name__ == "__main__":
    # Ensure the script runs from its directory so the db file is created there
    # Get the directory of the current script
    script_dir = os.path.dirname(os.path.abspath(__file__))
    db_path = os.path.join(script_dir, DATABASE_NAME)

    # You might want to clean the db file for a fresh start each time during testing
    # if os.path.exists(db_path):
    #     os.remove(db_path)
    #     print(f"Removed existing database: {db_path}")

    conn = create_connection(db_path)

    if conn:
        create_table(conn)

        # Basic CRUD Operations Demonstration

        # Insert
        insert_product(conn, "Laptop", 1200.50)
        insert_product(conn, "Keyboard", 75.00)
        product3_id = insert_product(conn, "Mouse", 25.99)

        # Read
        select_all_products(conn)

        # Update
        if product3_id is not None:
             update_product_price(conn, product3_id, 22.50)
             select_all_products(conn) # Read again to see the update

        # Delete
        # Let's delete the Keyboard (assuming it was the second inserted)
        # A better way is to select by name or use the ID returned by insert
        # For demonstration, let's just delete the one we know the ID of (the Mouse, product3_id)
        if product3_id is not None:
            delete_product(conn, product3_id)
            select_all_products(conn) # Read again to see the deletion

        # Close the connection
        conn.close()
        print(f"Database connection closed for {DATABASE_NAME}.")
    else:
        print("Failed to create database connection.")