import time
import threading

class DatabaseConnection:
    def __enter__(self):
        print("Opening database connection...")
        time.sleep(0.5)
        self.connection = "Connection established"
        return self.connection

    def __exit__(self, exc_type, exc_value, traceback):
        print("Closing database connection...")
        time.sleep(0.3)
        if exc_type:
            print(f"Error during operation: {exc_value}")

def perform_db_operation():
    with DatabaseConnection() as conn:
        print(f"Performing operation with: {conn}")
        # Simulate a database operation
        time.sleep(1)
        # raise ValueError("Database error occurred") # Uncomment to test error handling

perform_db_operation()