import sqlite3
import os

DATABASE_NAME = "multi_table_transaction_demo.db"

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
    """ Creates orders and order_details tables """
    create_orders_table_sql = """
    CREATE TABLE IF NOT EXISTS orders (
        order_id INTEGER PRIMARY KEY AUTOINCREMENT,
        customer_id INTEGER,
        order_date TEXT NOT NULL,
        total_amount REAL NOT NULL DEFAULT 0.0
    );
    """

    create_order_details_table_sql = """
    CREATE TABLE IF NOT EXISTS order_details (
        detail_id INTEGER PRIMARY KEY AUTOINCREMENT,
        order_id INTEGER NOT NULL,
        product_name TEXT NOT NULL,
        quantity INTEGER NOT NULL CHECK(quantity > 0),
        price_per_item REAL NOT NULL CHECK(price_per_item >= 0),
        FOREIGN KEY (order_id) REFERENCES orders (order_id) ON DELETE CASCADE
    );
    """
    try:
        cursor = conn.cursor()
        cursor.execute(create_orders_table_sql)
        cursor.execute(create_order_details_table_sql)
        conn.commit()
        print("Tables 'orders' and 'order_details' checked/created.")
    except sqlite3.Error as e:
        print(f"Error setting up tables: {e}")
        conn.rollback()

def add_order_with_details(conn, customer_id, order_date, items, cause_error=False):
    """
    Adds a new order and its details in a single transaction.
    Items should be a list of tuples: [(product_name, quantity, price_per_item), ...]
    If cause_error is True, an error is introduced after adding some details.
    """
    print(f"\n--- Attempting to Add Order for Customer {customer_id} ---")
    try:
        with conn: 
            print("  Transaction started for adding order...")
            cursor = conn.cursor()

            # 1. Insert into orders table
            insert_order_sql = "INSERT INTO orders (customer_id, order_date) VALUES (?, ?);"
            cursor.execute(insert_order_sql, (customer_id, order_date))
            order_id = cursor.lastrowid
            print(f"  Inserted new order with ID: {order_id}")

            # 2. Insert into order_details table
            insert_detail_sql = "INSERT INTO order_details (order_id, product_name, quantity, price_per_item) VALUES (?, ?, ?, ?);"
            total_amount = 0.0
            for i, (product_name, quantity, price_per_item) in enumerate(items):
                if cause_error and i == 1: 
                    print(f"  Simulating an error after item {i+1}: {product_name}")
                    raise ValueError("Simulated processing error!")

                print(f"  Adding detail for product: {product_name}")
                cursor.execute(insert_detail_sql, (order_id, product_name, quantity, price_per_item))
                total_amount += quantity * price_per_item

            # 3. Update the total amount in the orders table (if no error occurred)
            update_order_total_sql = "UPDATE orders SET total_amount = ? WHERE order_id = ?;"
            cursor.execute(update_order_total_sql, (total_amount, order_id))
            print(f"  Updated order {order_id} total amount: {total_amount}")

            print("Transaction block finished.")

    except (sqlite3.Error, ValueError) as e: 
        print(f"  Caught an error during transaction: {e}")
        print("  Transaction automatically rolled back by the 'with conn:' context manager.")
        order_id = None 

    except Exception as e:
         print(f"  Caught an unexpected error during transaction: {e}")
         print("  Transaction automatically rolled back by the 'with conn:' context manager.")
         order_id = None

    return order_id


def check_table_counts(conn):
    """ Prints the number of rows in orders and order_details tables """
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM orders;")
        order_count = cursor.fetchone()[0]
        cursor.execute("SELECT COUNT(*) FROM order_details;")
        detail_count = cursor.fetchone()[0]
        print(f"Current counts: orders = {order_count}, order_details = {detail_count}")
    except sqlite3.Error as e:
        print(f"Error checking counts: {e}")


if __name__ == "__main__":
    script_dir = os.path.dirname(os.path.abspath(__file__))
    db_path = os.path.join(script_dir, DATABASE_NAME)

    if os.path.exists(db_path):
        os.remove(db_path)
        print(f"Removed existing database: {db_path}")

    conn = create_connection(db_path)

    if conn:
        setup_tables(conn)
        check_table_counts(conn)

        items_for_failed_order = [
            ("Product 1A", 1, 10.00),
            ("Product 1B", 2, 5.00), 
            ("Product 1C", 3, 20.00),
        ]
        failed_order_id = add_order_with_details(conn, 101, "2023-10-27", items_for_failed_order, cause_error=True)

        if failed_order_id is None:
            print("\nOrder creation failed as expected due to simulated error.")
        check_table_counts(conn) 

        items_for_successful_order = [
            ("Product 2A", 5, 8.00),
            ("Product 2B", 1, 15.00),
            ("Product 2C", 2, 12.50),
        ]
        successful_order_id = add_order_with_details(conn, 102, "2023-10-28", items_for_successful_order, cause_error=False)

        if successful_order_id is not None:
            print(f"\nOrder created successfully with ID: {successful_order_id}")

        check_table_counts(conn)


        conn.close()
        print(f"\nDatabase connection closed for {DATABASE_NAME}.")
    else:
        print("Failed to create database connection.")