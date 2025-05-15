# level_up_drills/05_concurrency_handling/transfers.py

# --- DIAGNOSTIC ADDITION: Explicitly add parent directory to sys.path ---
# This is a workaround for environments where python -m doesn't automatically
# add the package root (the directory containing shared.py for this package)
# to sys.path correctly.
import sys
import os

# Get the directory of the current script (05_concurrency_handling)
script_dir = os.path.dirname(os.path.abspath(__file__))
# Get the parent directory (level_up_drills)
parent_dir = os.path.dirname(script_dir)
# Add the parent directory to sys.path. This should be the directory containing shared.py for this package.
sys.path.insert(0, parent_dir)
print(f"DEBUG: Added {parent_dir} to sys.path for import.")
# --- END DIAGNOSTIC ADDITION ---


# This script demonstrates concurrency issues in banking transfers
# and how to solve them with pessimistic locking (SELECT FOR UPDATE).

# Requires PostgreSQL for with_for_update() support.
# Update shared.py DATABASE_URL to PostgreSQL.

# Import necessary components and the MODEL from shared.py
# REMOVE 'Base' and 'create_tables' from this import, as the model definition should be ONLY in shared.py.
from shared import SessionLocal, engine, Account # Use appropriate SessionLocal/engine and import Account model

from sqlalchemy import Column, Integer, String, Float # Still needed for types if defining elsewhere or for context
from sqlalchemy.orm import Session # For type hinting
import threading # To simulate concurrent access
import time # To add delays and highlight race conditions
from typing import Optional

# --- REMOVE ACCOUNT MODEL DEFINITION FROM HERE ---
# The definition of class Account(Base): ... should be ONLY in shared.py.
# Delete that entire class definition block from THIS file.


# Ensure tables exist (run once before starting transfers)
# ... (comments on running create_tables) ...

# --- Helper to setup initial accounts ---
# Note: This uses a dialect-specific insert (ON CONFLICT) which requires
# the dialect-specific insert functions to be imported or handled.
# Ensure shared.py imports those or handle them here if needed.
from sqlalchemy.dialects.postgresql import insert as postgres_insert # For PG
from sqlalchemy.dialects.sqlite import insert as sqlite_insert     # For SQLite
from sqlalchemy.dialects import postgresql, sqlite                 # For dialect checking

def setup_initial_accounts():
    db = SessionLocal()
    try:
        accounts_data = [
            {"account_id": 101, "account_holder": "Alice", "balance": 1000.00},
            {"account_id": 102, "account_holder": "Bob", "balance": 500.00},
            # Corrected Charlie's entry
            {"account_id": 103, "account_holder": "Charlie", "balance": 200.00},
        ]

        # Use the correct dialect-specific insert function
        if isinstance(engine.dialect, postgresql.dialect):
             insert_func = postgres_insert
        elif isinstance(engine.dialect, sqlite.dialect):
             insert_func = sqlite_insert
        else:
             print(f"Unsupported dialect for ON CONFLICT setup: {engine.dialect.name}")
             return

        # Use ON CONFLICT DO NOTHING on account_id (primary key) to avoid errors if accounts already exist
        insert_stmt = insert_func(Account).values(accounts_data).on_conflict_do_nothing(index_elements=['account_id'])

        db.execute(insert_stmt)
        db.commit()
        print("Initial accounts setup.")
    except Exception as e:
        db.rollback()
        print(f"Error setting up initial accounts: {e}")
    finally:
        db.close()

def get_account_balance(account_id: int) -> Optional[float]:
    """Fetches the balance for an account."""
    db = SessionLocal()
    try:
        # Need to query the Account model which is imported
        account = db.query(Account.balance).filter(Account.account_id == account_id).first()
        return account[0] if account else None
    except Exception as e:
        print(f"Error fetching balance for account {account_id}: {e}")
        return None
    finally:
        db.close()

def print_balances():
     db = SessionLocal()
     try:
         # Need to query the Account model which is imported
         accounts = db.query(Account).order_by(Account.account_id).all()
         print("\n--- Account Balances ---")
         for acc in accounts:
             # Ensure Account model has __repr__ or access attributes like acc.account_id, acc.balance
             print(f"Account {acc.account_id} ({acc.account_holder}): ${acc.balance:.2f}")
         print("------------------------")
     finally:
         db.close()

# --- Naive (Buggy) Transfer - Subject to Race Conditions ---
def naive_transfer(from_account_id: int, to_account_id: int, amount: float):
    """
    Attempts to transfer funds naively (prone to lost updates).
    DO NOT USE IN PRODUCTION.
    """
    print(f"  Naive Transfer {from_account_id} -> {to_account_id} amount {amount} START")
    db = SessionLocal()
    try:
        # Need to query the Account model which is imported
        from_account = db.query(Account).filter(Account.account_id == from_account_id).first()
        to_account = db.query(Account).filter(Account.account_id == to_account_id).first()

        if not from_account or not to_account:
             print(f"  Naive Transfer {amount} FAILED: Account not found")
             db.rollback()
             return False

        # Simulate a delay BEFORE the update happens
        # This increases the chance of a race condition
        time.sleep(0.1)

        if from_account.balance < amount:
            print(f"  Naive Transfer {amount} FAILED: Insufficient funds in {from_account_id}")
            db.rollback()
            return False

        # --- Potential Lost Update Here ---
        from_account.balance -= amount
        to_account.balance += amount

        db.commit()
        print(f"  Naive Transfer {amount} from {from_account_id} to {to_account_id} COMPLETED.")
        return True
    except Exception as e:
         print(f"  Naive Transfer {amount} FAILED unexpectedly: {e}")
         db.rollback()
         return False
    finally:
        db.close()


# --- Correct Transfer with Pessimistic Locking (SELECT FOR UPDATE) ---
def correct_transfer_pessimistic(from_account_id: int, to_account_id: int, amount: float):
    """
    Transfers funds using SELECT FOR UPDATE (pessimistic locking).
    Requires database support (like PostgreSQL).
    """
    print(f"  Correct Transfer {from_account_id} -> {to_account_id} amount {amount} START")
    db = SessionLocal() # Use the appropriate SessionLocal
    try:
        # Start a transaction (SQLA session handles this)

        # 1. SELECT and acquire locks on the accounts
        # Use with_for_update() to acquire row-level pessimistic locks
        # Other transactions attempting to SELECT FOR UPDATE or modify these rows will WAIT.
        # Need to query the Account model which is imported
        from_account = db.query(Account)\
                         .filter(Account.account_id == from_account_id)\
                         .with_for_update()\
                         .first()

        # Lock the destination account too! Ordering locks consistently can prevent deadlocks.
        # Sort accounts by ID before locking if possible to reduce deadlock risk.
        account_ids = sorted([from_account_id, to_account_id])
        if from_account_id != account_ids[0]: # If from_account wasn't the first ID
             # Re-fetch in sorted order if necessary
             ordered_accounts = db.query(Account)\
                                  .filter(Account.account_id.in_(account_ids))\
                                  .order_by(Account.account_id)\
                                  .with_for_update()\
                                  .all()
             from_account = ordered_accounts[0] if ordered_accounts[0].account_id == from_account_id else ordered_accounts[1]
             to_account = ordered_accounts[0] if ordered_accounts[0].account_id == to_account_id else ordered_accounts[1]

        else: # from_account was the first ID, just fetch the second one
             to_account = db.query(Account)\
                            .filter(Account.account_id == to_account_id)\
                            .with_for_update()\
                            .first()


        if not from_account or not to_account:
             print(f"  Correct Transfer {amount} FAILED: Account not found")
             db.rollback() # Release locks and rollback
             return False

        # Simulate a delay AFTER acquiring locks but BEFORE the update
        # Locks prevent other transactions from interfering during this delay
        time.sleep(0.1)


        if from_account.balance < amount:
            print(f"  Correct Transfer {amount} FAILED: Insufficient funds in {from_account_id}")
            db.rollback() # Release locks and rollback
            return False

        # --- Safe Update ---
        # Because of the locks, the balance read here is guaranteed to be the latest committed value.
        from_account.balance -= amount
        to_account.balance += amount

        db.commit() # Release locks and commit
        print(f"  Correct Transfer {amount} from {from_account_id} to {to_account_id} COMPLETED.")
        return True
    except Exception as e:
         print(f"  Correct Transfer {amount} FAILED unexpectedly: {e}")
         db.rollback() # Release locks and rollback
         return False
    finally:
        db.close()

# --- Simulation of Concurrent Access ---
def simulate_concurrent_transfers(transfer_func, transfers):
    threads = []
    for from_acc, to_acc, amount in transfers:
        # Create a thread for each transfer
        thread = threading.Thread(target=transfer_func, args=(from_acc, to_acc, amount))
        threads.append(thread)

    start_time = time.time()
    # Start all threads
    for thread in threads:
        thread.start()

    # Wait for all threads to complete
    for thread in threads:
        thread.join()

    end_time = time.time()
    print(f"\nSimulation finished in {end_time - start_time:.2f} seconds.")


if __name__ == "__main__":
    # Ensure Account table exists
    # Add Account model to your shared.py Base.metadata
    # and run create_tables() or create_async_tables() once.
    # Ensure shared.py is configured for PostgreSQL.

    # Set up initial accounts (run once before simulations)
    setup_initial_accounts()

    # --- Scenario 1: Naive Transfers (Demonstrates Race Condition) ---
    print("\n--- Running Naive Concurrent Transfers ---")
    print_balances() # Initial balances

    # Define transfers that hit the same source account concurrently
    naive_transfers_list = [
        (101, 102, 100.00), # Alice -> Bob 100
        (101, 103, 50.00)   # Alice -> Charlie 50
        # Expected: Alice's balance goes down by 150 (to 850)
        # Naive might end up with Alice's balance as 900 or 950 due to lost update
    ]
    simulate_concurrent_transfers(naive_transfer, naive_transfers_list)

    print_balances() # Check balances after naive transfers (Alice's balance might be wrong)

    # Reset balances for the next test
    setup_initial_accounts() # Re-run setup to reset

    # --- Scenario 2: Correct Transfers with Pessimistic Locking ---
    print("\n--- Running Correct Concurrent Transfers (Pessimistic Locking) ---")
    print_balances() # Initial balances

    correct_transfers_list = [
        (101, 102, 100.00), # Alice -> Bob 100
        (101, 103, 50.00)   # Alice -> Charlie 50
        # Expected: Alice's balance goes down by 150 (to 850)
    ]
    # ensure shared.py is using PostgreSQL before running this simulation
    # if "postgresql" in str(engine.url): # Check if engine is for PG
    simulate_concurrent_transfers(correct_transfer_pessimistic, correct_transfers_list)
    # else:
    #     print("Skipping correct_transfer_pessimistic simulation because shared.py is not configured for PostgreSQL.")

    print_balances() # Check balances after correct transfers (Alice's balance should be correct: 850.00)

    # Note: For a simple SQLite setup, SELECT FOR UPDATE is not available.
    # An alternative concurrency strategy for SQLite or other DBs without FOR UPDATE
    # is Optimistic Concurrency Control (e.g., using version numbers and retries).