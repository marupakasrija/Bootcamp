# 05_inventory_transaction/inventory_transaction.py
import sqlite3
import os
import time

# Define a database file name for this specific demo
DATABASE_NAME = "inventory_transaction_demo.db"

def create_connection(db_file):
    """ Creates a database connection """
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        # Enable foreign key constraint enforcement (if applicable, less critical here)
        conn.execute("PRAGMA foreign_keys = ON;")
        # print(f"Connected to database: {db_file}")
        return conn
    except sqlite3.Error as e:
        print(f"Error connecting to database: {e}")
        return None

def setup_tables(conn):
    """ Creates products and inventory_log tables and populates products """
    create_products_table_sql = """
    CREATE TABLE IF NOT EXISTS products (
        product_id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL UNIQUE,
        stock_quantity INTEGER NOT NULL CHECK(stock_quantity >= 0) -- Ensure quantity is non-negative
    );
    """

    create_inventory_log_table_sql = """
    CREATE TABLE IF NOT EXISTS inventory_log (
        log_id INTEGER PRIMARY KEY AUTOINCREMENT,
        product_id INTEGER NOT NULL,
        change_quantity INTEGER NOT NULL, -- Negative for sale, positive for restock
        log_time TEXT NOT NULL,
        notes TEXT,
        FOREIGN KEY (product_id) REFERENCES products (product_id)
    );
    """
    try:
        cursor = conn.cursor()
        cursor.execute(create_products_table_sql)
        cursor.execute(create_inventory_log_table_sql)

        # Clear existing data and populate with sample products
        cursor.execute("DELETE FROM products;")
        cursor.execute("DELETE FROM inventory_log;")
        cursor.execute("INSERT INTO products (name, stock_quantity) VALUES (?, ?);", ("Widget", 50))
        cursor.execute("INSERT INTO products (name, stock_quantity) VALUES (?, ?);", ("Gadget", 30))
        cursor.execute("INSERT INTO products (name, stock_quantity) VALUES (?, ?);", ("Thing", 10))

        conn.commit()
        print("Tables 'products' and 'inventory_log' checked/created and products populated.")
    except sqlite3.Error as e:
        print(f"Error setting up tables: {e}")
        conn.rollback()

def get_product_stock(conn, product_name):
    """ Fetches the current stock quantity for a product by name """
    sql = "SELECT stock_quantity FROM products WHERE name = ?;"
    try:
        cursor = conn.cursor()
        cursor.execute(sql, (product_name,))
        result = cursor.fetchone()
        return result[0] if result else None # Return quantity or None if product not found
    except sqlite3.Error as e:
        print(f"Error fetching stock for product '{product_name}': {e}")
        return None

def process_sale(conn, product_name, quantity_sold, cause_log_error=False):
    """
    Processes a sale transaction: decrease stock and log the transaction.
    If cause_log_error is True, simulates an error during logging.
    """
    print(f"\n--- Attempting to process sale: {quantity_sold} of '{product_name}' ---")
    if quantity_sold <= 0:
        print("  Quantity sold must be positive.")
        return False

    try:
        with conn: # Start transaction
            print("  Transaction started for sale processing...")
            cursor = conn.cursor()

            # 1. Get current stock and product ID
            print(f"  Checking stock for '{product_name}'...")
            cursor.execute("SELECT product_id, stock_quantity FROM products WHERE name = ?;", (product_name,))
            product_info = cursor.fetchone()

            if product_info is None:
                raise ValueError(f"Product '{product_name}' not found.")
            product_id, current_stock = product_info

            if current_stock < quantity_sold:
                raise ValueError(f"Insufficient stock for '{product_name}'. Available: {current_stock}, Needed: {quantity_sold}")

            # 2. Update stock quantity in the products table
            new_stock = current_stock - quantity_sold
            print(f"  Updating stock for '{product_name}' (ID {product_id}): {current_stock} -> {new_stock}")
            update_stock_sql = "UPDATE products SET stock_quantity = ? WHERE product_id = ?;"
            cursor.execute(update_stock_sql, (new_stock, product_id))

            # 3. Log the sale in the inventory_log table
            log_quantity_change = -quantity_sold # Sales are negative changes
            log_time = time.strftime('%Y-%m-%d %H:%M:%S')
            log_notes = f"Sale of {quantity_sold} units"

            print(f"  Logging sale for '{product_name}' (Change: {log_quantity_change})...")

            # Simulate an error during logging if requested
            if cause_log_error:
                 print("  Simulating a logging error...")
                 # Attempt to insert invalid data, e.g., text into an INTEGER column if the table structure allowed,
                 # or just raise a Python error. Let's raise a Python error.
                 raise RuntimeError("Simulated logging system failure!")

            insert_log_sql = "INSERT INTO inventory_log (product_id, change_quantity, log_time, notes) VALUES (?, ?, ?, ?);"
            cursor.execute(insert_log_sql, (product_id, log_quantity_change, log_time, log_notes))
            log_id = cursor.lastrowid
            print(f"  Logged sale with ID: {log_id}")


            print("  Transaction block finished successfully.")
            # If no exception, conn.commit() happens automatically
            return True # Indicate success

    except (sqlite3.Error, ValueError, RuntimeError) as e: # Catch DB errors and our custom errors
        print(f"  Caught an error during sale processing: {e}")
        print("  Transaction automatically rolled back by the 'with conn:' context manager.")
        return False # Indicate failure

    except Exception as e:
         print(f"  Caught an unexpected error during sale processing: {e}")
         print("  Transaction automatically rolled back by the 'with conn:' context manager.")
         return False


def check_table_counts(conn):
    """ Prints the number of rows in products and inventory_log tables """
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM products;")
        product_count = cursor.fetchone()[0]
        cursor.execute("SELECT COUNT(*) FROM inventory_log;")
        log_count = cursor.fetchone()[0]
        print(f"\nCurrent counts: products = {product_count}, inventory_log = {log_count}")
    except sqlite3.Error as e:
        print(f"Error checking counts: {e}")


# --- Main Execution ---
if __name__ == "__main__":
    script_dir = os.path.dirname(os.path.abspath(__file__))
    db_path = os.path.join(script_dir, DATABASE_NAME)

    # Clean up the database file for a fresh start
    if os.path.exists(db_path):
        os.remove(db_path)
        print(f"Removed existing database: {db_path}")

    conn = create_connection(db_path)

    if conn:
        setup_tables(conn)
        check_table_counts(conn)

        # --- Display initial stock ---
        print("\n--- Initial Stock ---")
        print(f"Widget: {get_product_stock(conn, 'Widget')}")
        print(f"Gadget: {get_product_stock(conn, 'Gadget')}")
        print(f"Thing: {get_product_stock(conn, 'Thing')}")


        # --- Demonstrate Successful Sale ---
        process_sale(conn, "Widget", 10)
        print("\n--- Stock & Log Count After Successful Sale ---")
        print(f"Widget: {get_product_stock(conn, 'Widget')}")
        check_table_counts(conn)


        # --- Demonstrate Failed Sale (Insufficient Stock) ---
        process_sale(conn, "Thing", 20) # Thing only has 10 in stock
        print("\n--- Stock & Log Count After Insufficient Stock Attempt ---")
        print(f"Thing: {get_product_stock(conn, 'Thing')}") # Should be unchanged
        check_table_counts(conn) # Log count should also be unchanged


        # --- Demonstrate Failed Sale (Simulated Logging Error) ---
        # Sell a smaller quantity that *is* in stock, but cause a log error
        process_sale(conn, "Gadget", 5, cause_log_error=True)
        print("\n--- Stock & Log Count After Simulated Logging Error Attempt ---")
        print(f"Gadget: {get_product_stock(conn, 'Gadget')}") # Should be unchanged
        check_table_counts(conn) # Log count should also be unchanged


        # --- Demonstrate Another Successful Sale ---
        process_sale(conn, "Gadget", 5, cause_log_error=False) # This time it should succeed
        print("\n--- Stock & Log Count After Second Successful Sale ---")
        print(f"Gadget: {get_product_stock(conn, 'Gadget')}") # Should be updated
        check_table_counts(conn) # Log count should increase


        conn.close()
        print(f"\nDatabase connection closed for {DATABASE_NAME}.")
    else:
        print("Failed to create database connection.")