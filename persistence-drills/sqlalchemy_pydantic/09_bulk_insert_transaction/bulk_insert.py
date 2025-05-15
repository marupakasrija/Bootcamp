# sqlalchemy_pydantic/09_bulk_insert_transaction/bulk_insert.py

# --- DIAGNOSTIC ADDITION: Explicitly add parent directory to sys.path ---
import sys
import os

# Get the directory of the current script (09_bulk_insert_transaction)
script_dir = os.path.dirname(os.path.abspath(__file__))
# Get the parent directory (sqlalchemy_pydantic)
parent_dir = os.path.dirname(script_dir)
# Add the parent directory to sys.path. This should be the directory containing shared.py.
sys.path.insert(0, parent_dir)
print(f"DEBUG: Added {parent_dir} to sys.path for import.")
# --- END DIAGNOSTIC ADDITION ---


from shared import SessionLocal, User, UserCreate
from typing import List
from sqlalchemy.exc import IntegrityError

def bulk_create_users(users_data: List[UserCreate]) -> bool:
    """
    Inserts multiple users in a single transaction.

    Args:
        users_data: A list of Pydantic UserCreate models.

    Returns:
        True if all users were inserted successfully, False otherwise.
    """
    db = SessionLocal()
    try:
        # Start a transaction (SQLAlchemy sessions manage transactions by default,
        # commit() ends it successfully, rollback() ends it on failure)
        # Explicit BEGIN is not typically needed with SQLAlchemy sessions.

        # Convert list of Pydantic models to list of SQLAlchemy models
        db_users = [User(name=user_data.name, email=user_data.email) for user_data in users_data]

        db.add_all(db_users) # Add all objects to the session

        db.commit() # Commit the transaction

        print(f"Successfully inserted {len(users_data)} users in bulk.")
        return True

    except IntegrityError as e:
        db.rollback() # Rollback the entire transaction if any integrity error occurs
        print(f"Bulk insert failed due to Integrity Error (e.g., duplicate email): {e}")
        return False
    except Exception as e:
        db.rollback() # Rollback for any other error
        print(f"An unexpected error occurred during bulk insert: {e}")
        return False
    finally:
        db.close()

# Helper to fetch and print users (can reuse code from fetch_all.py if needed)
# For this script, we'll just use a local print function
def get_users_for_print():
    # Assuming User and SessionLocal are imported via the diagnostic path
    db = SessionLocal()
    try:
        users = db.query(User).all()
        # Need UserSchema here too for Pydantic conversion if desired
        # from shared import UserSchema # Import UserSchema here or at the top if needed
        # return [UserSchema.model_validate(user) for user in users] # V2
        # return [UserSchema.from_orm(user) for user in users] # V1
        return users # Return raw SQLAlchemy objects for simpler printing
    finally:
        db.close()

def print_all_users():
    all_users = get_users_for_print()
    if all_users:
        print("\n--- All Users in DB ---")
        for user in all_users: # Printing SQLAlchemy object representation
            print(user) # Requires __repr__ in User model
            # Or print attributes: print(f"ID: {user.id}, Name: {user.name}, Email: {user.email}")
        print("-----------------------")
    else:
        print("\nNo users found in the database.")


if __name__ == "__main__":
    # Make sure you have users in the database (run 02_insert_user/insert.py if needed)
    # Note: If running against PostgreSQL, ensure shared.py DATABASE_URL is updated

    # Example 1: Valid bulk insert
    valid_users_to_add = [
        UserCreate(name="David", email="david@example.com"),
        UserCreate(name="Eve", email="eve@example.com"),
        UserCreate(name="Frank", email="frank@example.com"),
    ]

    print("\nAttempting valid bulk insert...")
    bulk_create_users(valid_users_to_add)
    print_all_users() # Check if D, E, F were added

    # Example 2: Bulk insert with a duplicate email (should rollback the whole batch)
    invalid_users_to_add = [
        UserCreate(name="Grace", email="grace@example.com"),
        UserCreate(name="Alice Again", email="alice.new@example.com"), # Assuming alice.new@example.com exists from Drill 5
        UserCreate(name="Heidi", email="heidi@example.com"),
    ]

    print("\nAttempting bulk insert with a duplicate email...")
    bulk_create_users(invalid_users_to_add)

    # Fetch and print all users again - Grace and Heidi should NOT be in the list if rollback worked
    print("\nUsers after attempted invalid bulk insert:")
    print_all_users()