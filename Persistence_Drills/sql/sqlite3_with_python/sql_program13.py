import sqlite3
import os

DATABASE_NAME = "store_aggregation.db"

class ProductDBWithAggregation:
    def __init__(self, db_name=DATABASE_NAME):
        self.db_name = db_name
        self._ensure_table_exists()
        self._add_initial_data() # Add some data

    def _connect(self):
        conn = None
        try:
            conn = sqlite3.connect(self.db_name)
            return conn
        except sqlite3.Error as e:
            print(f"Database connection error: {e}")
            if conn: conn.close()
            return None

    def _ensure_table_exists(self):
        conn = self._connect()
        if conn:
            try:
                cursor = conn.cursor()
                create_table_sql = """
                CREATE TABLE IF NOT EXISTS products (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL UNIQUE,
                    price REAL NOT NULL CHECK (price >= 0)
                );
                """
                cursor.execute(create_table_sql)
                conn.commit()
            except sqlite3.Error as e:
                print(f"Error ensuring table exists: {e}")
                if conn: conn.rollback()
            finally:
                if conn: conn.close()

    def _add_initial_data(self):
         conn = self._connect()
         if conn:
             try:
                 cursor = conn.cursor()
                 add_product_sql = "INSERT OR IGNORE INTO products (name, price) VALUES (?, ?);"
                 products_to_add = [
                     ("Widget A", 10.50),
                     ("Widget B", 20.00),
                     ("Widget C", 5.75),
                     ("Widget D", 30.00),
                 ]
                 cursor.executemany(add_product_sql, products_to_add)
                 conn.commit()
                 # print("Initial data added for aggregation.")
             except sqlite3.Error as e:
                 print(f"Error adding initial data: {e}")
                 if conn: conn.rollback()
             finally:
                 if conn: conn.close()

    def calculate_total_inventory_value(self):
        """Calculates the sum of prices of all products."""
        conn = self._connect()
        total_value = 0.0
        if conn:
            try:
                cursor = conn.cursor()
                # Use the SUM() aggregation function
                sql = "SELECT SUM(price) FROM products;"
                cursor.execute(sql)
                # fetchone() retrieves a single row (in this case, a single value)
                result = cursor.fetchone()
                if result and result[0] is not None: # Check if there's a result and it's not NULL (empty table)
                    total_value = result[0]

            except sqlite3.Error as e:
                print(f"Error calculating total value: {e}")
            finally:
                if conn:
                    conn.close()
        return total_value

    # ... (Include other methods like print_products if needed)

# --- Exercise Execution ---
if __name__ == "__main__":
    product_db = ProductDBWithAggregation()

    # Calculate and print the total value
    total_value = product_db.calculate_total_inventory_value()
    print(f"\nTotal value of all products in inventory: ${total_value:.2f}")

    # Add another product and recalculate
    product_db.add_product("Widget E", 15.25)
    total_value_after_add = product_db.calculate_total_inventory_value()
    print(f"Total value after adding Widget E: ${total_value_after_add:.2f}")


    # Clean up (optional)
    # if os.path.exists(DATABASE_NAME):
    #     os.remove(DATABASE_NAME)
    #     print(f"\nRemoved database file {DATABASE_NAME}")