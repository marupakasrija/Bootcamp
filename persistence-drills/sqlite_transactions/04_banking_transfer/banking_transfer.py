import sqlite3
import os

DATABASE_NAME = "banking_transaction_demo.db"

def create_connection(db_file):
    """ Creates a database connection """
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        return conn
    except sqlite3.Error as e:
        print(f"Error connecting to database: {e}")
        return None

def setup_accounts_table(conn):
    """ Creates the accounts table and populates it """
    create_accounts_table_sql = """
    CREATE TABLE IF NOT EXISTS accounts (
        account_id INTEGER PRIMARY KEY,
        account_holder TEXT NOT NULL,
        balance REAL NOT NULL CHECK(balance >= 0) -- Ensure balance is non-negative
    );
    """
    try:
        cursor = conn.cursor()
        cursor.execute(create_accounts_table_sql)

        cursor.execute("DELETE FROM accounts;")
        cursor.execute("INSERT INTO accounts (account_id, account_holder, balance) VALUES (?, ?, ?);", (101, "Alice", 1000.00))
        cursor.execute("INSERT INTO accounts (account_id, account_holder, balance) VALUES (?, ?, ?);", (102, "Bob", 500.00))
        cursor.execute("INSERT INTO accounts (account_id, account_holder, balance) VALUES (?, ?, ?);", (103, "Charlie", 200.00))

        conn.commit()
        print("Accounts table checked/created and populated with sample data.")
    except sqlite3.Error as e:
        print(f"Error setting up accounts table: {e}")
        conn.rollback()

def get_account_balance(conn, account_id):
    """ Fetches the balance for a given account ID """
    sql = "SELECT balance FROM accounts WHERE account_id = ?;"
    try:
        cursor = conn.cursor()
        cursor.execute(sql, (account_id,))
        result = cursor.fetchone()
        return result[0] if result else None
    except sqlite3.Error as e:
        print(f"Error fetching balance for account {account_id}: {e}")
        return None


def transfer_funds(conn, from_account_id, to_account_id, amount, cause_error=False):
    """
    Transfers funds from one account to another within a transaction.
    If cause_error is True, simulates an error after debiting.
    """
    print(f"\n--- Attempting to Transfer {amount:.2f} from {from_account_id} to {to_account_id} ---")
    if amount <= 0:
        print("  Transfer amount must be positive.")
        return False

    try:
        with conn: 
            print("  Transaction started for fund transfer...")
            cursor = conn.cursor()

            # 1. Check if the source account exists and has sufficient balance
            print(f"  Checking balance for account {from_account_id}...")
            cursor.execute("SELECT balance FROM accounts WHERE account_id = ?;", (from_account_id,))
            from_balance_row = cursor.fetchone()

            if from_balance_row is None:
                raise ValueError(f"Source account {from_account_id} not found.")
            from_balance = from_balance_row[0]

            if from_balance < amount:
                raise ValueError(f"Insufficient balance in account {from_account_id}. Available: {from_balance:.2f}, Needed: {amount:.2f}")

            # 2. Debit the source account
            print(f"  Debiting {amount:.2f} from account {from_account_id}...")
            update_debit_sql = "UPDATE accounts SET balance = balance - ? WHERE account_id = ?;"
            cursor.execute(update_debit_sql, (amount, from_account_id))

            # 3. Simulate an error AFTER debiting but BEFORE crediting (to test rollback)
            if cause_error:
                print(f"  Simulating an error after debiting account {from_account_id}...")
                raise RuntimeError("Simulated network error during credit!")

            # 4. Check if the destination account exists
            print(f"  Checking destination account {to_account_id}...")
            cursor.execute("SELECT account_id FROM accounts WHERE account_id = ?;", (to_account_id,))
            to_account_row = cursor.fetchone()
            if to_account_row is None:
                 raise ValueError(f"Destination account {to_account_id} not found.")


            # 5. Credit the destination account
            print(f"  Crediting {amount:.2f} to account {to_account_id}...")
            update_credit_sql = "UPDATE accounts SET balance = balance + ? WHERE account_id = ?;"
            cursor.execute(update_credit_sql, (amount, to_account_id))

            print("  Transaction block finished successfully.")
            return True 

    except (sqlite3.Error, ValueError, RuntimeError) as e: 
        print(f"  Caught an error during transfer: {e}")
        print("  Transaction automatically rolled back by the 'with conn:' context manager.")
        return False 

    except Exception as e:
         print(f"  Caught an unexpected error during transfer: {e}")
         print("  Transaction automatically rolled back by the 'with conn:' context manager.")
         return False


if __name__ == "__main__":
    script_dir = os.path.dirname(os.path.abspath(__file__))
    db_path = os.path.join(script_dir, DATABASE_NAME)

    if os.path.exists(db_path):
        os.remove(db_path)
        print(f"Removed existing database: {db_path}")

    conn = create_connection(db_path)

    if conn:
        setup_accounts_table(conn)

        print("\n--- Initial Balances ---")
        print(f"Alice (101): {get_account_balance(conn, 101):.2f}")
        print(f"Bob (102): {get_account_balance(conn, 102):.2f}")
        print(f"Charlie (103): {get_account_balance(conn, 103):.2f}")


        transfer_funds(conn, 101, 102, 300.00, cause_error=True)

        print("\n--- Balances After Failed Transfer Attempt ---")
        print(f"Alice (101): {get_account_balance(conn, 101):.2f}")
        print(f"Bob (102): {get_account_balance(conn, 102):.2f}")
        print(f"Charlie (103): {get_account_balance(conn, 103):.2f}")


        transfer_funds(conn, 101, 102, 200.00, cause_error=False)

        print("\n--- Balances After Successful Transfer ---")
        print(f"Alice (101): {get_account_balance(conn, 101):.2f}")
        print(f"Bob (102): {get_account_balance(conn, 102):.2f}")
        print(f"Charlie (103): {get_account_balance(conn, 103):.2f}")

        transfer_funds(conn, 101, 103, 900.00, cause_error=False) # Alice only has 800 left

        print("\n--- Balances After Insufficient Funds Attempt ---")
        print(f"Alice (101): {get_account_balance(conn, 101):.2f}")
        print(f"Bob (102): {get_account_balance(conn, 102):.2f}")
        print(f"Charlie (103): {get_account_balance(conn, 103):.2f}")


        conn.close()
        print(f"\nDatabase connection closed for {DATABASE_NAME}.")
    else:
        print("Failed to create database connection.")