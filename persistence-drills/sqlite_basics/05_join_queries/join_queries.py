# 05_join_queries/join_queries.py
import sqlite3
import os

# Define the database file name
DATABASE_NAME = "store.db"

def create_connection(db_file):
    """ Creates a database connection """
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        # print(f"Connected to database: {db_file}")
        conn.execute("PRAGMA foreign_keys = ON;") # Enable foreign key support
        return conn
    except sqlite3.Error as e:
        print(f"Error connecting to database: {e}")
        return None

def setup_tables(conn):
    """ Creates categories and products tables """
    create_categories_table_sql = """
    CREATE TABLE IF NOT EXISTS categories (
        category_id INTEGER PRIMARY KEY AUTOINCREMENT,
        category_name TEXT NOT NULL UNIQUE
    );
    """

    # Add category_id column and foreign key constraint to products table
    # Note: Modifying existing tables needs care. If the table exists without
    # the category_id, you'd typically do:
    # 1. ALTER TABLE ADD COLUMN
    # 2. Update existing rows
    # 3. ALTER TABLE ADD CONSTRAINT (Foreign Key)
    # For simplicity here, we'll assume a fresh start or handle the ALTER IF needed.
    # Let's create a products table specifically for this script if it doesn't exist,
    # including the foreign key. This avoids issues if run after 02/03 without cleanup.

    create_products_table_sql = """
    CREATE TABLE IF NOT EXISTS products (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL UNIQUE,
        price REAL NOT NULL CHECK (price >= 0),
        category_id INTEGER, -- New column
        FOREIGN KEY (category_id) REFERENCES categories (category_id) -- Foreign key constraint
    );
    """
    try:
        cursor = conn.cursor()
        cursor.execute(create_categories_table_sql)
        cursor.execute(create_products_table_sql)
        conn.commit()
        print("Tables 'categories' and 'products' checked/created.")
    except sqlite3.Error as e:
        print(f"Error setting up tables: {e}")
        conn.rollback()

def add_category(conn, category_name):
    """ Adds a new category """
    sql = "INSERT OR IGNORE INTO categories (category_name) VALUES (?);" # IGNORE if exists
    try:
        cursor = conn.cursor()
        cursor.execute(sql, (category_name,))
        conn.commit()
        category_id = cursor.lastrowid if cursor.rowcount > 0 else None
        if category_id:
             print(f"Added category: {category_name} with ID {category_id}")
        else:
             # If rowcount is 0, it means the category already existed due to UNIQUE constraint
             cursor.execute("SELECT category_id FROM categories WHERE category_name = ?", (category_name,))
             category_id = cursor.fetchone()[0]
             print(f"Category already exists: {category_name} with ID {category_id}")

        return category_id
    except sqlite3.Error as e:
        print(f"Error adding category: {e}")
        conn.rollback()
        return None

def add_product_with_category(conn, name, price, category_id):
    """ Adds a product linked to a category """
    # Basic validation for category_id existence could be added here,
    # but the FOREIGN KEY constraint handles it at the DB level.
    sql = "INSERT INTO products (name, price, category_id) VALUES (?, ?, ?);"
    try:
        cursor = conn.cursor()
        cursor.execute(sql, (name, price, category_id))
        conn.commit()
        product_id = cursor.lastrowid
        print(f"Added product: '{name}' (ID {product_id}) linked to category ID {category_id}")
        return product_id
    except sqlite3.IntegrityError as ie:
        print(f"Integrity Error adding product '{name}': {ie} (e.g., name exists or invalid category_id)")
        conn.rollback()
        return None
    except sqlite3.Error as e:
        print(f"Error adding product '{name}': {e}")
        conn.rollback()
        return None


def get_products_with_categories(conn):
    """ Fetches products with their category names using a JOIN """
    sql = """
    SELECT
        p.id,
        p.name AS product_name,
        p.price,
        c.category_name
    FROM products p
    JOIN categories c ON p.category_id = c.category_id;
    """
    try:
        cursor = conn.cursor()
        cursor.execute(sql)
        rows = cursor.fetchall()
        return rows
    except sqlite3.Error as e:
        print(f"Error executing JOIN query: {e}")
        return []


# --- Main Execution ---
if __name__ == "__main__":
    script_dir = os.path.dirname(os.path.abspath(__file__))
    db_path = os.path.join(script_dir, DATABASE_NAME)

    # Clean up the database file for a fresh start for THIS script's demo
    # Note: If you want to use data from 02 or 03, comment this out,
    # but ensure products in 02/03 didn't have the category_id column,
    # or handle the ALTER TABLE migration in setup_tables.
    if os.path.exists(db_path):
         os.remove(db_path)
         print(f"Removed existing database: {db_path}")


    conn = create_connection(db_path)

    if conn:
        setup_tables(conn)

        # Add Categories
        electronics_id = add_category(conn, "Electronics")
        books_id = add_category(conn, "Books")
        furniture_id = add_category(conn, "Furniture")
        # Add again to show IGNORE
        add_category(conn, "Electronics")

        # Add Products with Categories
        if electronics_id is not None:
             add_product_with_category(conn, "Laptop", 1200.50, electronics_id)
             add_product_with_category(conn, "Keyboard", 75.00, electronics_id)
        if books_id is not None:
             add_product_with_category(conn, "Python Guide", 45.00, books_id)
             add_product_with_category(conn, "SQL Basics", 30.00, books_id)

        # Attempt to add a product with an invalid category ID (will fail due to FOREIGN KEY)
        add_product_with_category(conn, "Invalid Product", 10.00, 999)


        # Perform and print the JOIN query results
        print("\n--- Products with Categories ---")
        products_with_categories = get_products_with_categories(conn)
        if products_with_categories:
            for p in products_with_categories:
                print(f"ID: {p[0]}, Name: {p[1]}, Price: {p[2]}, Category: {p[3]}")
        else:
            print("No products found with categories.")

        # Close the connection
        conn.close()
        print(f"\nDatabase connection closed for {DATABASE_NAME}.")
    else:
        print("Failed to create database connection.")