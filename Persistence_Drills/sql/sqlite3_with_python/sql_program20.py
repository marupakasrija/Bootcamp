import sqlite3
import os
import datetime

DATABASE_NAME = "inventory_transaction.db"

def setup_inventory_tables():
    """Creates products and inventory_log tables."""
    conn = None
    try:
        conn = sqlite3.connect(DATABASE_NAME)
        cursor = conn.cursor()

        create_products_sql = """
        CREATE TABLE IF NOT EXISTS products (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL UNIQUE,
            stock INTEGER NOT NULL CHECK (stock >= 0) -- Stock cannot be negative
        );
        """
        cursor.execute(create_products_sql)

        create_log_sql = """
        CREATE TABLE IF NOT EXISTS inventory_log (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            product_id INTEGER,
            change_amount INTEGER NOT NULL, -- Positive for added, negative for removed
            timestamp TEXT NOT NULL,
            notes TEXT,
            FOREIGN KEY (product_id) REFERENCES products(id)
        );
        """
        cursor.execute(create_log_sql)

        conn.commit()
        print(f"Tables 'products' and 'inventory_log' ensured in '{DATABASE_NAME}'.")

        # Add some initial products (use INSERT OR IGNORE)
        initial_products_sql = "INSERT OR IGNORE INTO products (id, name, stock) VALUES (?, ?, ?);"
        products_data = [(1, "Widget X", 100), (2, "Gadget Y", 50), (3, "Thing Z", 200)]
        cursor.executemany(initial_products_sql, products_data)
        conn.commit()
        print("Initial products added.")

    except sqlite3.Error as e:
        print(f"Error setting up inventory tables: {e}")
        if conn: conn.rollback()
    finally:
        if conn: conn.close()

def update_inventory_and_log(product_id, change_amount, notes=""):
    """Updates product stock and logs the change in a transaction."""
    # Basic validation
    if not isinstance(product_id, int) or product_id <= 0:
         print("Inventory Update Error: Product ID must be a positive integer.")
         return False
    if not isinstance(change_amount, int):
         print("Inventory Update Error: Change amount must be an integer.")
         return False
    if not isinstance(notes, str):
         print("Inventory Update Error: Notes must be a string.")
         return False


    conn = None
    try:
        conn = sqlite3.connect(DATABASE_NAME)
        cursor = conn.cursor()

        # Start a transaction
        conn.execute("BEGIN;")

        # 1. Update the product stock
        update_stock_sql = "UPDATE products SET stock = stock + ? WHERE id = ?;"
        cursor.execute(update_stock_sql, (change_amount, product_id))

        # Check if the product was found and updated
        if cursor.rowcount == 0:
             raise ValueError(f"Product with ID {product_id} not found.")

        # Check for negative stock after the update (if change_amount was negative)
        # This relies on the CHECK constraint on the 'stock' column,
        # which will raise an IntegrityError if violated upon commit.
        # Alternatively, you could SELECT the stock here and check manually.

        # 2. Log the inventory change
        log_change_sql = """
        INSERT INTO inventory_log (product_id, change_amount, timestamp, notes)
        VALUES (?, ?, ?, ?);
        """
        current_timestamp = datetime.datetime.now().isoformat()
        cursor.execute(log_change_sql, (product_id, change_amount, current_timestamp, notes))

        # Simulate a log insertion failure for testing:
        # For example, try inserting with a non-existent product_id if FOREIGN KEY constraint is active.
        # if product_id == 999:
        #     cursor.execute(log_change_sql, (999, change_amount, current_timestamp, "Simulated log failure"))


        # If both operations (update and log) succeed, commit
        conn.commit()
        print(f"Inventory updated for product ID {product_id} by {change_amount}. Logged.")
        return True

    except ValueError as e:
         # Catch validation or "product not found" errors
         print(f"Inventory Update Failed (transaction rolled back): {e}")
         if conn: conn.rollback()
         return False
    except sqlite3.IntegrityError as e:
        # Catches errors like negative stock due to CHECK constraint or FOREIGN KEY violation
        print(f"Database Integrity Error during Inventory Update (transaction rolled back): {e}")
        if conn: conn.rollback()
        return False
    except sqlite3.Error as e:
        # Catch any other database errors
        print(f"Database Error during Inventory Update (transaction rolled back): {e}")
        if conn: conn.rollback()
        return False
    finally:
        if conn:
            conn.close()

def get_product_stock(product_id):
    """Fetches the current stock for a product."""
    conn = None
    stock = None
    try:
        conn = sqlite3.connect(DATABASE_NAME)
        cursor = conn.cursor()
        sql = "SELECT stock FROM products WHERE id = ?;"
        cursor.execute(sql, (product_id,))
        result = cursor.fetchone()
        if result:
            stock = result[0]
    except sqlite3.Error as e:
        print(f"Error fetching stock for product {product_id}: {e}")
    finally:
        if conn: conn.close()
    return stock

def get_inventory_log(product_id=None):
     """Fetches inventory log entries."""
     conn = None
     log_entries = []
     try:
         conn = sqlite3.connect(DATABASE_NAME)
         conn.row_factory = sqlite3.Row
         cursor = conn.cursor()
         sql = "SELECT * FROM inventory_log"
         params = ()
         if product_id is not None:
              sql += " WHERE product_id = ?"
              params = (product_id,)
         sql += " ORDER BY timestamp DESC;"
         cursor.execute(sql, params)
         log_entries = cursor.fetchall()
     except sqlite3.Error as e:
         print(f"Error fetching inventory log: {e}")
     finally:
         if conn: conn.close()
     return log_entries

def print_inventory_status():
    """Prints current product stock and recent log entries."""
    conn = None
    try:
        conn = sqlite3.connect(DATABASE_NAME)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        print("\n--- Current Inventory Stock ---")
        cursor.execute("SELECT id, name, stock FROM products ORDER BY id;")
        products = cursor.fetchall()
        if products:
             for p in products:
                  print(f"ID: {p['id']}, Name: {p['name']}, Stock: {p['stock']}")
        else:
             print("No products found.")
        print("-------------------------------")

        print("\n--- Recent Inventory Log Entries ---")
        log_entries = get_inventory_log()
        if log_entries:
             for log in log_entries:
                  print(f"[{log['timestamp']}] Product ID {log['product_id']}, Change: {log['change_amount']}, Notes: '{log['notes']}'")
        else:
             print("No log entries found.")
        print("------------------------------------")

    except sqlite3.Error as e:
        print(f"Error printing inventory status: {e}")
    finally:
        if conn: conn.close()


# --- Exercise Execution ---
if __name__ == "__main__":
    setup_inventory_tables()
    print_inventory_status()

    # Perform a valid inventory update (reduce stock)
    print("\nAttempting valid inventory update (Reduce Widget X stock by 10):")
    update_inventory_and_log(1, -10, "Sale")
    print_inventory_status() # Widget X stock should be 90, log entry added

    # Perform a valid inventory update (increase stock)
    print("\nAttempting valid inventory update (Increase Gadget Y stock by 20):")
    update_inventory_and_log(2, 20, "Restock")
    print_inventory_status() # Gadget Y stock should be 70, log entry added

    # Attempt an update that would result in negative stock
    print("\nAttempting inventory update resulting in negative stock (Reduce Widget X by 100):")
    update_inventory_and_log(1, -100, "Attempted large withdrawal") # Widget X is at 90
    print_inventory_status() # Stock should remain 90, no new log entry due to rollback

    # Attempt an update for a non-existent product
    print("\nAttempting inventory update for non-existent product (ID 999):")
    update_inventory_and_log(999, 50, "Received for unknown product")
    print_inventory_status() # No change to stock or log due to rollback

    # Clean up (optional)
    # if os.path.exists(DATABASE_NAME):
    #     os.remove(DATABASE_NAME)
    #     print(f"\nRemoved database file {DATABASE_NAME}")