import sqlite3
import os

DATABASE_NAME = "store.db"

def create_connection(db_file):
    """ Creates a database connection """
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        conn.execute("PRAGMA foreign_keys = ON;") 
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


if __name__ == "__main__":
    script_dir = os.path.dirname(os.path.abspath(__file__))
    db_path = os.path.join(script_dir, DATABASE_NAME)

    if os.path.exists(db_path):
         os.remove(db_path)
         print(f"Removed existing database: {db_path}")


    conn = create_connection(db_path)

    if conn:
        setup_tables(conn)

        electronics_id = add_category(conn, "Electronics")
        books_id = add_category(conn, "Books")
        furniture_id = add_category(conn, "Furniture")
        add_category(conn, "Electronics")

        if electronics_id is not None:
             add_product_with_category(conn, "Laptop", 1200.50, electronics_id)
             add_product_with_category(conn, "Keyboard", 75.00, electronics_id)
        if books_id is not None:
             add_product_with_category(conn, "Python Guide", 45.00, books_id)
             add_product_with_category(conn, "SQL Basics", 30.00, books_id)

        add_product_with_category(conn, "Invalid Product", 10.00, 999)


        print("\n--- Products with Categories ---")
        products_with_categories = get_products_with_categories(conn)
        if products_with_categories:
            for p in products_with_categories:
                print(f"ID: {p[0]}, Name: {p[1]}, Price: {p[2]}, Category: {p[3]}")
        else:
            print("No products found with categories.")

        conn.close()
        print(f"\nDatabase connection closed for {DATABASE_NAME}.")
    else:
        print("Failed to create database connection.")