import sqlite3
import os

DATABASE_NAME = "multi_table_transaction.db"

def setup_order_tables():
    """Creates orders and order_details tables."""
    conn = None
    try:
        conn = sqlite3.connect(DATABASE_NAME)
        cursor = conn.cursor()

        create_orders_sql = """
        CREATE TABLE IF NOT EXISTS orders (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            customer_name TEXT NOT NULL,
            order_date TEXT,
            total_amount REAL DEFAULT 0.0
        );
        """
        cursor.execute(create_orders_sql)

        create_order_details_sql = """
        CREATE TABLE IF NOT EXISTS order_details (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            order_id INTEGER,
            product_name TEXT NOT NULL,
            quantity INTEGER NOT NULL CHECK (quantity > 0),
            price_per_item REAL NOT NULL CHECK (price_per_item >= 0),
            FOREIGN KEY (order_id) REFERENCES orders(id) ON DELETE CASCADE
        );
        """
        # ON DELETE CASCADE means if an order is deleted, its details are automatically deleted.
        cursor.execute(create_order_details_sql)

        conn.commit()
        print(f"Tables 'orders' and 'order_details' ensured in '{DATABASE_NAME}'.")
    except sqlite3.Error as e:
        print(f"Error setting up order tables: {e}")
        if conn: conn.rollback()
    finally:
        if conn: conn.close()

def place_order_in_transaction(customer_name, order_items):
    """Places an order, inserting into orders and order_details in a transaction."""
    conn = None
    try:
        conn = sqlite3.connect(DATABASE_NAME)
        cursor = conn.cursor()

        # Start a transaction
        conn.execute("BEGIN;")

        # 1. Insert into the 'orders' table
        insert_order_sql = "INSERT INTO orders (customer_name, order_date) VALUES (?, date('now'));"
        cursor.execute(insert_order_sql, (customer_name,))
        order_id = cursor.lastrowid # Get the ID of the newly inserted order

        # 2. Prepare data for 'order_details'
        details_to_insert = []
        total_amount = 0.0
        for item in order_items:
            # Basic validation for item structure
            if len(item) != 3 or not isinstance(item[0], str) or not isinstance(item[1], int) or not isinstance(item[2], (int, float)):
                raise ValueError(f"Invalid order item format: {item}. Expected (product_name, quantity, price_per_item).")

            product_name, quantity, price_per_item = item
            details_to_insert.append((order_id, product_name, quantity, price_per_item))
            total_amount += quantity * price_per_item

        # 3. Insert into the 'order_details' table
        insert_detail_sql = """
        INSERT INTO order_details (order_id, product_name, quantity, price_per_item)
        VALUES (?, ?, ?, ?);
        """
        cursor.executemany(insert_detail_sql, details_to_insert)

        # 4. Update the 'total_amount' in the 'orders' table (optional but good practice)
        update_order_total_sql = "UPDATE orders SET total_amount = ? WHERE id = ?;"
        cursor.execute(update_order_total_sql, (total_amount, order_id))


        # If all steps succeeded, commit the transaction
        conn.commit()
        print(f"Order placed successfully for {customer_name} with Order ID {order_id}. Total: ${total_amount:.2f}")
        return order_id

    except ValueError as e:
        # Catch validation errors specifically
        print(f"Validation Error placing order (transaction rolled back): {e}")
        if conn:
            conn.rollback()
        return None
    except sqlite3.Error as e:
        # Catch any database errors and rollback
        print(f"Database Error placing order (transaction rolled back): {e}")
        if conn:
            conn.rollback()
        return None
    finally:
        # Ensure the connection is closed
        if conn:
            conn.close()

def get_order_details(order_id):
     """Fetches details for a specific order."""
     conn = None
     order_info = None
     details = []
     try:
         conn = sqlite3.connect(DATABASE_NAME)
         conn.row_factory = sqlite3.Row # Access columns by name
         cursor = conn.cursor()

         # Fetch order header
         cursor.execute("SELECT * FROM orders WHERE id = ?;", (order_id,))
         order_info = cursor.fetchone()

         if order_info:
              # Fetch order details
              cursor.execute("SELECT * FROM order_details WHERE order_id = ?;", (order_id,))
              details = cursor.fetchall()

     except sqlite3.Error as e:
         print(f"Error fetching order details for ID {order_id}: {e}")
     finally:
         if conn: conn.close()

     return order_info, details

def print_order(order_info, order_details):
     if order_info:
          print("\n--- Order Details ---")
          print(f"Order ID: {order_info['id']}")
          print(f"Customer: {order_info['customer_name']}")
          print(f"Date: {order_info['order_date']}")
          print(f"Total: ${order_info['total_amount']:.2f}")
          print("Items:")
          if order_details:
               for item in order_details:
                    print(f"  - {item['quantity']}x {item['product_name']} @ ${item['price_per_item']:.2f}")
          else:
               print("  No items found.")
          print("---------------------")
     else:
          print("\nOrder not found.")


# --- Exercise Execution ---
if __name__ == "__main__":
    setup_order_tables()

    # Place a valid order
    order_items_1 = [
        ("Laptop", 1, 1200.00),
        ("Mouse", 2, 25.00),
    ]
    order_id_1 = place_order_in_transaction("Alice", order_items_1)

    if order_id_1:
        order_info_1, details_1 = get_order_details(order_id_1)
        print_order(order_info_1, details_1)


    # Attempt to place an order with invalid data (e.g., negative quantity)
    print("\nAttempting to place order with invalid item data:")
    order_items_2 = [
        ("Keyboard", 1, 70.00),
        ("Monitor", -1, 150.00), # Invalid quantity
        ("Webcam", 1, 50.00)
    ]
    order_id_2 = place_order_in_transaction("Bob", order_items_2)

    if not order_id_2:
        print("Order failed as expected. Checking if partial data was inserted...")
        # You can manually check the database file using the sqlite3 command line
        # SELECT * FROM orders;
        # SELECT * FROM order_details;
        pass # No order should exist for Bob


    # Clean up (optional)
    # if os.path.exists(DATABASE_NAME):
    #     os.remove(DATABASE_NAME)
    #     print(f"\nRemoved database file {DATABASE_NAME}")