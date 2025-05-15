# level_up_drills/03_idempotent_upserts/upsert_product.py

# --- DIAGNOSTIC ADDITION: Explicitly add parent directory to sys.path ---
# This is a workaround for environments where python -m doesn't automatically
# add the package root (the directory containing shared.py for this package)
# to sys.path correctly.
import sys
import os

# Get the directory of the current script (03_idempotent_upserts)
script_dir = os.path.dirname(os.path.abspath(__file__))
# Get the parent directory (level_up_drills)
parent_dir = os.path.dirname(script_dir)
# Add the parent directory to sys.path. This should be the directory containing shared.py for this package.
sys.path.insert(0, parent_dir)
print(f"DEBUG: Added {parent_dir} to sys.path for import.")
# --- END DIAGNOSTIC ADDITION ---


# Import necessary components and the MODEL from shared.py
# REMOVE 'Base' from this import, as the model definition should be ONLY in shared.py.
from shared import SessionLocal, engine, create_tables, ProductForUpsert

from sqlalchemy import Column, Integer, String, Float # Still needed for types if defining elsewhere or for context
# Import dialect-specific insert constructs
from sqlalchemy.dialects.postgresql import insert as postgres_insert
from sqlalchemy.dialects.sqlite import insert as sqlite_insert
from sqlalchemy.dialects import postgresql, sqlite # Needed to check dialect name
from sqlalchemy.exc import NotSupportedError # Import NotSupportedError for handling


# --- REMOVE THE MODEL DEFINITION FROM HERE ---
# The definition of class ProductForUpsert(Base): ... should be ONLY in shared.py.
# Delete that entire class definition block from THIS file.


# Ensure tables exist (run once before upserting)
# You need to run create_tables() from shared.py after adding ProductForUpsert model to Base.metadata
# Example command (from the directory containing level_up_drills):
# python -m level_up_drills.shared # If shared.py has an if __name__ == "__main__": block that calls create_tables
# OR you can temporarily add a call to create_tables() in this script's __main__ block if needed for setup.


def upsert_product(name: str, price: float):
    """
    Inserts a product if it doesn't exist, or updates its price if it does.
    Uses ON CONFLICT ON CONSTRAINT for PostgreSQL/SQLite.
    """
    db = SessionLocal() # Use the appropriate SessionLocal (sync or async, matching shared.py)
    try:
        # Data to insert/update
        values = {"name": name, "price": price}

        # --- Construct the dialect-specific ON CONFLICT statement ---

        # --- Use the correct dialect-specific insert function to build the initial statement ---
        insert_stmt = None
        if isinstance(engine.dialect, postgresql.dialect):
             print(f"Using PostgreSQL dialect for upsert: '{engine.dialect.name}'")
             insert_stmt = postgres_insert(ProductForUpsert).values(**values)
        elif isinstance(engine.dialect, sqlite.dialect):
             print(f"Using SQLite dialect for upsert: '{engine.dialect.name}'")
             insert_stmt = sqlite_insert(ProductForUpsert).values(**values)
        else:
             # Raise an error or implement fallback logic for unsupported dialects
             db.rollback() # Ensure transaction is clean
             raise NotSupportedError(
                 f"Upserts with ON CONFLICT not directly supported for dialect: {engine.dialect.name}"
             )


        # --- Now call on_conflict_do_update on the dialect-specific insert object ---
        upsert_stmt = None # Reset upsert_stmt
        if isinstance(engine.dialect, postgresql.dialect):
             # PostgreSQL uses ON CONFLICT ON CONSTRAINT constraint_name DO UPDATE SET ...
             # Or ON CONFLICT (column_name) DO UPDATE SET ... Use index_elements for portability.
             upsert_stmt = insert_stmt.on_conflict_do_update(
                 index_elements=['name'], # Target the unique 'name' column
                 set_=dict(price=insert_stmt.excluded.price) # Update the price with the new price
                 # insert_stmt.excluded refers to the values proposed for insertion
             )
        elif isinstance(engine.dialect, sqlite.dialect):
             # SQLite uses ON CONFLICT (column_name) DO UPDATE SET ...
             upsert_stmt = insert_stmt.on_conflict_do_update(
                 index_elements=[ProductForUpsert.name], # Target the unique 'name' column using model attribute
                 set_=dict(price=insert_stmt.excluded.price) # Update the price
                 # SQLite's ON CONFLICT DO UPDATE automatically targets the conflicting row
             )
        # No 'else' needed here because the dialect was handled above


        # Execute the upsert statement
        result = db.execute(upsert_stmt)

        # ... (rest of try block: commit, print success) ...
        db.commit() # Commit the transaction
        print(f"Successfully upserted product: '{name}' with price {price}")


    except NotSupportedError as e:
        print(f"Configuration Error: {e}")
        # No rollback needed if an error is raised before DB interaction
        return False # Indicate failure
    except Exception as e:
        db.rollback()
        print(f"Error during upsert for product '{name}': {e}")
        return False
    finally:
        db.close()

# Helper to print products
def get_products_list():
    db = SessionLocal()
    products = db.query(ProductForUpsert).all() # Use the imported model
    db.close()
    return products

def print_products(products):
     if products:
         print("\n--- Products in upsert_product_table ---")
         for p in products:
              # The __repr__ method needs to be defined on the model in shared.py
              print(p)
         print("----------------")
     else:
         print("\nNo products found.")

if __name__ == "__main__":
    # Ensure ProductForUpsert table exists
    # Add ProductForUpsert model to your shared.py Base.metadata
    # and run create_tables() once before running this script.
    # You can add a temporary call here for setup if needed:
    # from shared import create_tables # Need to import create_tables
    # create_tables() # Call it once for setup

    # --- Example Usage ---

    # 1. Insert a new product
    print("Attempting to upsert 'Laptop'...")
    upsert_product("Laptop", 1200.50)
    print_products(get_products_list())

    # 2. Insert another new product
    print("\nAttempting to upsert 'Mouse'...")
    upsert_product("Mouse", 25.99)
    print_products(get_products_list())

    # 3. Update the price of an existing product ('Laptop')
    print("\nAttempting to upsert 'Laptop' with new price (update)...")
    upsert_product("Laptop", 1150.00) # New price
    print_products(get_products_list()) # Price of Laptop should be updated

    # 4. Insert a third new product
    print("\nAttempting to upsert 'Keyboard'...")
    upsert_product("Keyboard", 75.00)
    print_products(get_products_list())

    # 5. Update the price of another existing product ('Mouse')
    print("\nAttempting to upsert 'Mouse' with new price (update)...")
    upsert_product("Mouse", 28.00) # New price
    print_products(get_products_list()) # Price of Mouse should be updated