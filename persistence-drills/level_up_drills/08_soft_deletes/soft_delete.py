# level_up_drills/08_soft_deletes/soft_delete.py

# --- DIAGNOSTIC ADDITION: Explicitly add parent directory to sys.path ---
# This is a workaround for environments where python -m doesn't automatically
# add the package root (the directory containing shared.py for this package)
# to sys.path correctly.
import sys
import os

# Get the directory of the current script (08_soft_deletes)
script_dir = os.path.dirname(os.path.abspath(__file__))
# Get the parent directory (level_up_drills)
parent_dir = os.path.dirname(script_dir)
# Add the parent directory to sys.path. This should be the directory containing shared.py for this package.
sys.path.insert(0, parent_dir)
print(f"DEBUG: Added {parent_dir} to sys.path for import.")
# --- END DIAGNOSTIC ADDITION ---


# Import necessary components and the MODEL from shared.py
# REMOVE 'Base' and 'create_tables' from this import, as the model definition should be ONLY in shared.py.
from shared import SessionLocal, engine, ProductSoftDelete # Use appropriate SessionLocal/engine and import model

from sqlalchemy import Column, Integer, String, Float, DateTime # Still needed for types if defining elsewhere or for context
from sqlalchemy.orm import Session # For type hinting
import datetime # For timestamps
from typing import List, Optional
from sqlalchemy import or_ # Useful for complex filters including deleted items

# --- REMOVE MODEL DEFINITION FROM HERE ---
# The definition of class ProductSoftDelete(Base): ... should be ONLY in shared.py.
# Delete that entire class definition block from THIS file.


# Ensure tables exist (run once)
# ... (comments on running create_tables) ...

# --- Helper to add initial products ---
# Note: This uses a dialect-specific insert (ON CONFLICT) which requires
# the dialect-specific insert functions to be imported or handled.
# Ensure shared.py imports those or handle them here if needed.
from sqlalchemy.dialects.postgresql import insert as postgres_insert # For PG
from sqlalchemy.dialects.sqlite import insert as sqlite_insert     # For SQLite
from sqlalchemy.dialects import postgresql, sqlite                 # For dialect checking
from sqlalchemy.exc import IntegrityError # Needed for handling conflicts


def add_initial_products():
    db = SessionLocal()
    try:
        # Add some products for demonstration
        products_data = [
            {"id": 1, "name": "Laptop SD", "price": 1200.00, "deleted_at": None},
            {"id": 2, "name": "Keyboard SD", "price": 75.00, "deleted_at": None},
            {"id": 3, "name": "Mouse SD", "price": 25.00, "deleted_at": None},
        ]

        # Use the correct dialect-specific insert function for ON CONFLICT
        insert_func = None
        if isinstance(engine.dialect, postgresql.dialect):
             insert_func = postgres_insert
        elif isinstance(engine.dialect, sqlite.dialect):
             insert_func = sqlite_insert
        else:
             print(f"Warning: Unsupported dialect for ON CONFLICT setup: {engine.dialect.name}. Skipping initial product setup.")
             return

        # Use ON CONFLICT DO NOTHING on id (primary key) to avoid duplicates if run multiple times
        insert_stmt = insert_func(ProductSoftDelete).values(products_data).on_conflict_do_nothing(index_elements=['id'])

        db.execute(insert_stmt)
        db.commit()
        print("Initial products added for soft delete demo.")
    except IntegrityError as e:
         db.rollback()
         print(f"Products already exist (IntegrityError): {e}")
    except Exception as e:
        db.rollback()
        print(f"Error adding initial products: {e}")
    finally:
        db.close()

# --- Soft Delete / Restore Logic ---
def soft_delete_product(product_id: int) -> bool:
    """Marks a product as deleted by setting deleted_at timestamp."""
    db = SessionLocal() # Use the appropriate SessionLocal
    try:
        product = db.query(ProductSoftDelete).filter(ProductSoftDelete.id == product_id).first()
        if product:
            if product.deleted_at is None:
                product.deleted_at = datetime.datetime.now() # Set timestamp to mark as deleted
                db.commit()
                print(f"Soft deleted product ID {product_id} ('{product.name}').")
                return True
            else:
                print(f"Product ID {product_id} is already soft deleted.")
                return False
        else:
            print(f"Product ID {product_id} not found for soft delete.")
            return False
    except Exception as e:
        db.rollback() # Rollback if an error occurs
        print(f"Error soft deleting product ID {product_id}: {e}")
        return False
    finally:
        db.close()

def restore_product(product_id: int) -> bool:
    """Restores a soft-deleted product by setting deleted_at to NULL."""
    db = SessionLocal() # Use the appropriate SessionLocal
    try:
        # Note: We fetch regardless of deleted_at status here
        product = db.query(ProductSoftDelete).filter(ProductSoftDelete.id == product_id).first()
        if product:
            if product.deleted_at is not None:
                product.deleted_at = None # Set back to NULL to restore
                db.commit()
                print(f"Restored product ID {product_id} ('{product.name}').")
                return True
            else:
                print(f"Product ID {product_id} is not soft deleted.")
                return False
        else:
            print(f"Product ID {product_id} not found for restore.")
            return False
    except Exception as e:
        db.rollback()
        print(f"Error restoring product ID {product_id}: {e}")
        return False
    finally:
        db.close()

# --- Querying Logic ---
def get_active_products() -> List[ProductSoftDelete]:
    """Fetches only products where deleted_at IS NULL."""
    db = SessionLocal() # Use the appropriate SessionLocal
    try:
        # The core of soft delete: filter out where deleted_at is NOT NULL
        products = db.query(ProductSoftDelete)\
                     .filter(ProductSoftDelete.deleted_at.is_(None))\
                     .all()
        return products
    except Exception as e:
        print(f"Error fetching active products: {e}")
        return []
    finally:
        db.close()

def get_all_products_including_deleted() -> List[ProductSoftDelete]:
     """Fetches ALL products, regardless of deleted_at status."""
     db = SessionLocal() # Use the appropriate SessionLocal
     try:
         products = db.query(ProductSoftDelete).all() # No filter
         return products
     except Exception as e:
         print(f"Error fetching all products: {e}")
         return []
     finally:
         db.close()

def get_only_deleted_products() -> List[ProductSoftDelete]:
    """Fetches only products where deleted_at IS NOT NULL."""
    db = SessionLocal() # Use the appropriate SessionLocal
    try:
        products = db.query(ProductSoftDelete)\
                     .filter(ProductSoftDelete.deleted_at.isnot(None))\
                     .all()
        return products
    except Exception as e:
        print(f"Error fetching deleted products: {e}")
        return []
    finally:
        db.close()


# --- Cleanup / Hard Delete Logic ---
def hard_delete_old_soft_deleted_products(days_ago: int):
    """
    Permanently deletes products that were soft-deleted more than N days ago.
    This is typically run as a scheduled task (e.g., a nightly cron job).
    """
    db = SessionLocal() # Use the appropriate SessionLocal
    try:
        # Calculate the cutoff date
        cutoff_date = datetime.datetime.now() - datetime.timedelta(days=days_ago)

        # Find products that are soft-deleted AND older than the cutoff
        products_to_delete = db.query(ProductSoftDelete)\
                             .filter(ProductSoftDelete.deleted_at.isnot(None))\
                             .filter(ProductSoftDelete.deleted_at < cutoff_date)\
                             .all()

        count = len(products_to_delete)
        if count > 0:
            print(f"Found {count} products soft-deleted more than {days_ago} days ago. Deleting permanently...")
            # Note: For large datasets, you might use session.query(...).filter(...).delete(synchronize_session=False)
            # for a potentially more efficient bulk delete at the DB level.
            for product in products_to_delete:
                db.delete(product) # Mark for hard deletion
            db.commit() # Perform hard deletions in a single transaction
            print("Hard deletion complete.")
        else:
            print(f"No products soft-deleted more than {days_ago} days ago found to delete.")

    except Exception as e:
        db.rollback()
        print(f"Error during hard deletion: {e}")
    finally:
        db.close()


# Helper to print lists of products
def print_product_list(label: str, products: List[ProductSoftDelete]):
     print(f"\n--- {label} ---")
     if products:
         for p in products:
              print(p) # Uses the __repr__ method if defined on the model in shared.py
     else:
         print(f"No {label.lower().replace('---', '').strip()} found.")
     print("-" * (len(label) + 6))


if __name__ == "__main__":
    # Ensure ProductSoftDelete table exists
    # Add ProductSoftDelete model to your shared.py Base.metadata
    # and run create_tables() or create_async_tables() once before running this script.
    # You can add a temporary call here for setup if needed:
    # from shared import create_tables # Or create_async_tables
    # create_tables() # Call it once for setup

    # Add some initial data (run once or reset between tests)
    add_initial_products()

    # --- Demonstrate Soft Delete ---
    print_product_list("Initial Products", get_all_products_including_deleted())
    print_product_list("Active Products (filtered)", get_active_products())


    print("\n>>> Soft deleting Product ID 1 (Laptop SD)...")
    soft_delete_product(1)
    print_product_list("Products After Soft Delete", get_all_products_including_deleted())
    print_product_list("Active Products After Soft Delete", get_active_products())
    print_product_list("Deleted Products After Soft Delete", get_only_deleted_products())


    print("\n>>> Attempting to soft delete Product ID 1 again...")
    soft_delete_product(1) # Should print message about already deleted

    print("\n>>> Attempting to soft delete non-existent Product ID 999...")
    soft_delete_product(999)


    # --- Demonstrate Restore ---
    print("\n>>> Restoring Product ID 1 (Laptop SD)...")
    restore_product(1)
    print_product_list("Products After Restore", get_all_products_including_deleted())
    print_product_list("Active Products After Restore", get_active_products())
    print_product_list("Deleted Products After Restore", get_only_deleted_products())

    print("\n>>> Attempting to restore Product ID 1 again...")
    restore_product(1) # Should print message about not soft deleted

    print("\n>>> Attempting to restore non-existent Product ID 999...")
    restore_product(999)


    # --- Demonstrate Hard Delete (Conceptual) ---
    print("\n>>> Simulating Hard Delete of old records...")
    # Soft delete Product ID 2 and Product ID 3
    soft_delete_product(2)
    soft_delete_product(3)
    print_product_list("Products After Soft Deleting 2 and 3", get_all_products_including_deleted())
    print_product_list("Deleted Products", get_only_deleted_products())

    # To test hard delete, you would typically:
    # 1. Soft delete some items.
    # 2. Wait a sufficient amount of time (or manually edit the 'deleted_at' timestamp
    #    in the database to be in the past) so they are older than `days_ago`.
    # 3. Run hard_delete_old_soft_deleted_products(days_ago).

    print("\n(Hard delete requires items soft-deleted in the past or manual timestamp editing for testing.)")
    print("Attempting hard delete of items soft-deleted > 0 days ago (might delete 2 and 3 if run quickly):")
    hard_delete_old_soft_deleted_products(0) # Use 0 days ago for immediate testing

    print_product_list("Products After Attempted Hard Delete", get_all_products_including_deleted())