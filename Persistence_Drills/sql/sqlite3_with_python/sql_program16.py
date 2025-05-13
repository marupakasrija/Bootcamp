import sqlite3
import os

DATABASE_NAME = "basic_transaction.db"

def setup_customers_table():
    """Creates the customers table if it doesn't exist."""
    conn = None
    try:
        conn = sqlite3.connect(DATABASE_NAME)
        cursor = conn.cursor()
        create_table_sql = """
        CREATE TABLE IF NOT EXISTS customers (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL UNIQUE, -- Unique name to test errors
            email TEXT
        );
        """
        cursor.execute(create_table_sql)
        conn.commit()
        print(f"Table 'customers' ensured in '{DATABASE_NAME}'.")
    except sqlite3.Error as e:
        print(f"Error setting up customers table: {e}")
        if conn: conn.rollback()
    finally:
        if conn: conn.close()

def add_customers_in_transaction(customer_list):
    """Inserts a list of customers within a single transaction."""
    conn = None
    try:
        conn = sqlite3.connect(DATABASE_NAME)
        cursor = conn.cursor()

        # Explicitly begin a transaction
        conn.execute("BEGIN;") # This is often the default with sqlite3 if no other statements have run

        sql = "INSERT INTO customers (name, email) VALUES (?, ?);"
        cursor.executemany(sql, customer_list)

        # If all inserts succeed, commit the transaction
        conn.commit()
        print(f"Successfully added {len(customer_list)} customers in a transaction.")
        return True

    except sqlite3.Error as e:
        # If any error occurs during the transaction, rollback
        print(f"Error adding customers (transaction rolled back): {e}")
        if conn:
            conn.rollback() # Ensure rollback happens
        return False
    finally:
        # Ensure the connection is closed
        if conn:
            conn.close()

def get_all_customers():
    """Fetches all customers."""
    conn = None
    customers = []
    try:
        conn = sqlite3.connect(DATABASE_NAME)
        cursor = conn.cursor()
        sql = "SELECT id, name, email FROM customers;"
        cursor.execute(sql)
        customers = cursor.fetchall()
    except sqlite3.Error as e:
        print(f"Error fetching customers: {e}")
    finally:
        if conn: conn.close()
    return customers

def print_customers():
     customers = get_all_customers()
     if customers:
         print("\n--- Customers in DB ---")
         for customer in customers:
             print(f"ID: {customer[0]}, Name: {customer[1]}, Email: {customer[2]}")
         print("----------------------")
     else:
         print("\nNo customers in DB.")

# --- Exercise Execution ---
if __name__ == "__main__":
    setup_customers_table()

    # List of customers to add
    new_customers = [
        ("Alice", "alice@example.com"),
        ("Bob", "bob@example.com"),
        ("Charlie", "charlie@example.com"),
    ]

    # Add customers in a transaction
    add_customers_in_transaction(new_customers)
    print_customers()

    # Attempt to add customers including a duplicate name to trigger rollback
    print("\nAttempting to add customers with a duplicate (Bob):")
    customers_with_duplicate = [
        ("David", "david@example.com"),
        ("Bob", "bob_new@example.com"), # Duplicate name
        ("Eve", "eve@example.com"),
    ]
    add_customers_in_transaction(customers_with_duplicate)
    print_customers() # David and Eve should NOT be added if rollback worked

    # Clean up (optional)
    # if os.path.exists(DATABASE_NAME):
    #     os.remove(DATABASE_NAME)
    #     print(f"\nRemoved database file {DATABASE_NAME}")