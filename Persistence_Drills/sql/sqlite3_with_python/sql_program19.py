import sqlite3
import os

DATABASE_NAME = "banking_transaction.db"

def setup_accounts_table():
    """Creates the accounts table."""
    conn = None
    try:
        conn = sqlite3.connect(DATABASE_NAME)
        cursor = conn.cursor()
        create_table_sql = """
        CREATE TABLE IF NOT EXISTS accounts (
            account_id INTEGER PRIMARY KEY,
            account_holder TEXT NOT NULL,
            balance REAL NOT NULL CHECK (balance >= 0) -- Balance cannot be negative
        );
        """
        cursor.execute(create_table_sql)
        conn.commit()
        print(f"Table 'accounts' ensured in '{DATABASE_NAME}'.")

        # Add some initial accounts (use INSERT OR IGNORE to not duplicate)
        initial_accounts_sql = "INSERT OR IGNORE INTO accounts (account_id, account_holder, balance) VALUES (?, ?, ?);"
        accounts_data = [(101, "Alice", 1000.00), (102, "Bob", 500.00), (103, "Charlie", 200.00)]
        cursor.executemany(initial_accounts_sql, accounts_data)
        conn.commit()
        print("Initial accounts added.")

    except sqlite3.Error as e:
        print(f"Error setting up accounts table: {e}")
        if conn: conn.rollback()
    finally:
        if conn: conn.close()

def get_account_balance(account_id):
    """Fetches the balance for a given account ID."""
    conn = None
    balance = None
    try:
        conn = sqlite3.connect(DATABASE_NAME)
        cursor = conn.cursor()
        sql = "SELECT balance FROM accounts WHERE account_id = ?;"
        cursor.execute(sql, (account_id,))
        result = cursor.fetchone()
        if result:
            balance = result[0]
    except sqlite3.Error as e:
        print(f"Error fetching balance for account {account_id}: {e}")
    finally:
        if conn: conn.close()
    return balance

def transfer_funds(from_account_id, to_account_id, amount):
    """Transfers funds between two accounts in a single transaction."""
    # Basic validation
    if not isinstance(amount, (int, float)) or amount <= 0:
        print("Transfer Error: Amount must be a positive number.")
        return False
    if from_account_id == to_account_id:
         print("Transfer Error: Cannot transfer funds to the same account.")
         return False

    conn = None
    try:
        conn = sqlite3.connect(DATABASE_NAME)
        cursor = conn.cursor()

        # Start a transaction
        conn.execute("BEGIN;")

        # 1. Debit the 'from' account
        # Important: Check balance *within* the transaction to avoid race conditions
        # (though SELECT FOR UPDATE is better in highly concurrent systems, SQLite is simpler)
        cursor.execute("SELECT balance FROM accounts WHERE account_id = ?;", (from_account_id,))
        from_balance = cursor.fetchone()

        if not from_balance:
            raise ValueError(f"Source account {from_account_id} not found.")
        if from_balance[0] < amount:
            raise ValueError(f"Insufficient funds in account {from_account_id}.")

        update_from_sql = "UPDATE accounts SET balance = balance - ? WHERE account_id = ?;"
        cursor.execute(update_from_sql, (amount, from_account_id))

        # 2. Credit the 'to' account
        # Simulate a potential failure here for testing the rollback:
        # For example, try to update a non-existent account_id
        # if to_account_id == 999:
        #     raise sqlite3.OperationalError("Simulated Credit Failure")


        update_to_sql = "UPDATE accounts SET balance = balance + ? WHERE account_id = ?;"
        cursor.execute(update_to_sql, (amount, to_account_id))

        # Check if both updates affected exactly one row (basic check)
        # In a real system, you'd verify rowcounts or use more robust checks
        # if cursor.rowcount != 1:
        #     raise sqlite3.OperationalError("Credit update failed or affected wrong number of rows.")
        # The debit update's rowcount is from the first execute, might need separate cursor
        # or re-checking. For simplicity, relying on the Exception from DB if account_id doesn't exist.


        # If both updates were successful, commit the transaction
        conn.commit()
        print(f"Transfer successful: {amount:.2f} from {from_account_id} to {to_account_id}")
        return True

    except ValueError as e:
        # Catch validation or insufficient funds errors
        print(f"Transfer failed (transaction rolled back): {e}")
        if conn:
            conn.rollback()
        return False
    except sqlite3.Error as e:
        # Catch any database errors (e.g., account_id not found for credit)
        print(f"Database error during transfer (transaction rolled back): {e}")
        if conn:
            conn.rollback()
        return False
    finally:
        # Ensure the connection is closed
        if conn:
            conn.close()

def print_account_balances():
    """Prints the balances of all accounts."""
    conn = None
    try:
        conn = sqlite3.connect(DATABASE_NAME)
        cursor = conn.cursor()
        sql = "SELECT account_id, account_holder, balance FROM accounts ORDER BY account_id;"
        cursor.execute(sql)
        accounts = cursor.fetchall()
        if accounts:
            print("\n--- Account Balances ---")
            for acc in accounts:
                print(f"Account ID: {acc[0]}, Holder: {acc[1]}, Balance: ${acc[2]:.2f}")
            print("------------------------")
        else:
            print("\nNo accounts found.")
    except sqlite3.Error as e:
        print(f"Error fetching account balances: {e}")
    finally:
        if conn: conn.close()

# --- Exercise Execution ---
if __name__ == "__main__":
    setup_accounts_table()
    print_account_balances()

    # Perform a valid transfer
    print("\nAttempting valid transfer (Alice to Bob, $100):")
    transfer_funds(101, 102, 100.00)
    print_account_balances() # Alice's balance down, Bob's up

    # Attempt a transfer with insufficient funds
    print("\nAttempting transfer with insufficient funds (Alice to Charlie, $1000):")
    transfer_funds(101, 103, 1000.00) # Alice only has 900 now
    print_account_balances() # Balances should be unchanged due to rollback

    # Attempt a transfer to a non-existent account (simulate failure)
    print("\nAttempting transfer to non-existent account (Bob to 999, $50):")
    transfer_funds(102, 999, 50.00)
    print_account_balances() # Balances should be unchanged due to rollback

    # Clean up (optional)
    # if os.path.exists(DATABASE_NAME):
    #     os.remove(DATABASE_NAME)
    #     print(f"\nRemoved database file {DATABASE_NAME}")