# level_up_drills/09_large_dataset_testing/large_insert_test.py

# --- DIAGNOSTIC ADDITION: Explicitly add parent directory to sys.path ---
# This is a workaround for environments where python -m doesn't automatically
# add the package root (the directory containing shared.py for this package)
# to sys.path correctly.
import sys
import os

# Get the directory of the current script (09_large_dataset_testing)
script_dir = os.path.dirname(os.path.abspath(__file__))
# Get the parent directory (level_up_drills)
parent_dir = os.path.dirname(script_dir)
# Add the parent directory to sys.path. This should be the directory containing shared.py for this package.
sys.path.insert(0, parent_dir)
print(f"DEBUG: Added {parent_dir} to sys.path for import.")
# --- END DIAGNOSTIC ADDITION ---


# This script compares the performance of naive single inserts vs. batch inserts
# when dealing with a large number of records.

# Import necessary components and the MODEL from shared.py
# REMOVE 'Base' and 'create_tables' from this import, as the model definition should be ONLY in shared.py.
from shared import SessionLocal, engine, LargeProduct # Use appropriate SessionLocal/engine and import model

from sqlalchemy import Column, Integer, String, Float # Still needed for types if defining elsewhere or for context
from sqlalchemy.orm import Session # For type hinting
import time # For timing
import random # For generating test data
import string # For generating test data
import os # For database file size check (SQLite)
import sys # For observing process memory (less precise here)

# --- REMOVE MODEL DEFINITION FROM HERE ---
# The definition of class LargeProduct(Base): ... should be ONLY in shared.py.
# Delete that entire class definition block from THIS file.


# Ensure tables exist (run once)
# ... (comments on running create_tables) ...

# --- Helper to generate test data ---
def generate_random_string(length=10):
     letters = string.ascii_lowercase + string.ascii_uppercase + string.digits
     return ''.join(random.choice(letters) for i in range(length))

def generate_product_data(count: int):
    """Generates a list of dictionaries representing product data."""
    data = []
    # Using a set to track names to ensure uniqueness within the generated batch
    generated_names = set()
    print(f"Generating {count} test records...")
    for i in range(count):
        # Generate unique name
        name_prefix = f"TestProduct_{i}_"
        name_suffix = generate_random_string(random.randint(5, 10)) # Variable length suffix
        name = name_prefix + name_suffix
        # Regenerate suffix if name is not unique (simple approach)
        while name in generated_names:
             name_suffix = generate_random_string(random.randint(5, 10))
             name = name_prefix + name_suffix
        generated_names.add(name)

        price = round(random.uniform(1.0, 1000.0), 2)
        description = generate_random_string(random.randint(50, 200)) # Variable length description
        data.append({"name": name, "price": price, "description": description})

    print("Data generation complete.")
    return data

# --- Insertion Methods ---
def naive_single_inserts(data: list):
    """Inserts records one by one, committing each in its own transaction."""
    print("\n--- Running Naive Single Inserts ---")
    # Warning: This will be VERY slow for large datasets due to per-record transactions.
    db = SessionLocal()
    start_time = time.time()
    count = 0
    try:
        for item in data:
            # Create ORM object
            product = LargeProduct(name=item['name'], price=item['price'], description=item['description'])
            # Add to session
            db.add(product)
            # Commit immediately (new transaction for each)
            db.commit()
            count += 1
            if count % 1000 == 0: # Print progress every 1000 records
                print(f"  Inserted {count}/{len(data)}...")

        end_time = time.time()
        print(f"\nNaive single inserts: Inserted {count} records in {end_time - start_time:.2f} seconds.")
    except Exception as e:
        db.rollback()
        print(f"Error during naive insert after {count} records: {e}")
    finally:
        db.close()

def batch_inserts_with_transaction(data: list, batch_size: int = 5000):
    """Inserts records in batches within transactions."""
    print(f"\n--- Running Batch Inserts with Transaction (Batch Size: {batch_size}) ---")
    # This is generally much faster due to fewer transactions and network round trips.
    db = SessionLocal()
    start_time = time.time()
    total_count = 0
    try:
        # Start a single transaction for the entire operation or batches
        # Using batches with commits inside the loop can manage memory better for huge datasets
        # but committing once at the end is often fastest for reasonable dataset sizes.
        # Let's use batch commits here for memory management awareness.

        for i in range(0, len(data), batch_size):
            batch_data = data[i : i + batch_size]
            # Create ORM objects for the batch
            db_products = [
                LargeProduct(name=item['name'], price=item['price'], description=item['description'])
                for item in batch_data
            ]

            # Add all objects in the batch to the session
            db.add_all(db_products)

            # Commit the batch transaction
            # This flushes the changes to the database and starts a new transaction for the next batch.
            db.commit()

            total_count += len(batch_data)
            # Print progress based on total records committed
            print(f"  Committed batch up to {total_count}/{len(data)} ({len(batch_data)} in this batch)...")

        end_time = time.time()
        print(f"\nBatch inserts ({batch_size}/batch): Inserted {total_count} records in {end_time - start_time:.2f} seconds.")

    except Exception as e:
        # If an error occurs within a batch, only that batch's transaction is rolled back.
        # If you wanted the entire operation to be atomic, you would use a single transaction
        # around the entire loop and commit only at the very end.
        db.rollback()
        print(f"Error during batch insert after {total_count} records: {e}")
    finally:
        db.close()

def cleanup_data():
    """Deletes all data from the large test table."""
    db = SessionLocal()
    try:
        print("\nCleaning up test data...")
        # Use execute with a delete statement for efficient bulk deletion
        from sqlalchemy import delete
        delete_stmt = delete(LargeProduct)
        result = db.execute(delete_stmt)
        db.commit()
        print(f"Deleted {result.rowcount} records from {LargeProduct.__tablename__}.")
    except Exception as e:
        db.rollback()
        print(f"Error during cleanup: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    # Ensure LargeProduct table exists
    # Add LargeProduct model to your shared.py Base.metadata
    # and run create_tables() or create_async_tables() once before running this script.
    # You can add a temporary call here for setup if needed:
    # from shared import create_tables # Or create_async_tables
    # create_tables() # Call it once for setup

    # --- Configuration ---
    # Start with a smaller number (e.g., 10000) and increase gradually.
    # 1 million records might take a long time and consume significant resources.
    NUM_RECORDS = 100000 # Try 10k, 100k, 1M. Adjust down for faster tests.
    BATCH_SIZE = 5000 # Adjust batch size for batch inserts

    print(f"--- Performance Test with {NUM_RECORDS} Records ---")

    # --- Prepare Data ---
    test_data = generate_product_data(NUM_RECORDS)
    print(f"Generated {len(test_data)} records.")

    # --- Comparison ---

    # Clean up any previous data
    cleanup_data()

    # Run Naive Single Inserts
    # WARNING: This can take a very long time for large NUM_RECORDS
    naive_single_inserts(test_data)

    # Clean up before the next test
    cleanup_data()

    # Run Batch Inserts
    batch_inserts_with_transaction(test_data, batch_size=BATCH_SIZE)

    # --- Observe Performance and Memory ---
    # Timing is printed by the script.
    # To observe memory usage:
    # 1. Run the script from your terminal.
    # 2. Open your system's Task Manager (Windows) or htop/top (Linux/macOS).
    # 3. Look for the Python process that is running the script.
    # 4. Observe its memory usage during the insertion phase.
    # 5. Compare memory usage between the naive and batch methods.
    # Also observe disk I/O and CPU usage for the database process.
    print("\n--- Performance Test Complete ---")


    # Check final count (optional)
    db = SessionLocal()
    count = db.query(LargeProduct).count()
    db.close()
    print(f"\nFinal record count in table {LargeProduct.__tablename__}: {count}")