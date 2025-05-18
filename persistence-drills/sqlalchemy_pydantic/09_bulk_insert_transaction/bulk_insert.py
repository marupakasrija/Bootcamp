import sys
import os

script_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(script_dir)
sys.path.insert(0, parent_dir)
print(f"DEBUG: Added {parent_dir} to sys.path for import.")


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
        db_users = [User(name=user_data.name, email=user_data.email) for user_data in users_data]

        db.add_all(db_users) 

        db.commit()

        print(f"Successfully inserted {len(users_data)} users in bulk.")
        return True

    except IntegrityError as e:
        db.rollback() 
        print(f"Bulk insert failed due to Integrity Error (e.g., duplicate email): {e}")
        return False
    except Exception as e:
        db.rollback() 
        print(f"An unexpected error occurred during bulk insert: {e}")
        return False
    finally:
        db.close()
def get_users_for_print():
    db = SessionLocal()
    try:
        users = db.query(User).all()
    finally:
        db.close()

def print_all_users():
    all_users = get_users_for_print()
    if all_users:
        print("\n--- All Users in DB ---")
        for user in all_users: 
            print(user) 
        print("-----------------------")
    else:
        print("\nNo users found in the database.")


if __name__ == "__main__":
    # Example 1: Valid bulk insert
    valid_users_to_add = [
        UserCreate(name="David", email="david@example.com"),
        UserCreate(name="Eve", email="eve@example.com"),
        UserCreate(name="Frank", email="frank@example.com"),
    ]

    print("\nAttempting valid bulk insert...")
    bulk_create_users(valid_users_to_add)
    print_all_users() 

    # Example 2: Bulk insert with a duplicate email (should rollback the whole batch)
    invalid_users_to_add = [
        UserCreate(name="Grace", email="grace@example.com"),
        UserCreate(name="Alice Again", email="alice.new@example.com"), 
        UserCreate(name="Heidi", email="heidi@example.com"),
    ]

    print("\nAttempting bulk insert with a duplicate email...")
    bulk_create_users(invalid_users_to_add)
    print("\nUsers after attempted invalid bulk insert:")
    print_all_users()