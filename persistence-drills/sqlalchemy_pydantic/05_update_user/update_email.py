import sys
import os

script_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(script_dir)
sys.path.insert(0, parent_dir)
print(f"DEBUG: Added {parent_dir} to sys.path for import.")

from shared import SessionLocal, User, UserBase
from typing import Optional
from sqlalchemy.exc import IntegrityError

def update_user_email(user_id: int, new_email: str) -> bool:
    """
    Updates the email for a specific user.

    Args:
        user_id: The ID of the user to update.
        new_email: The new email address.

    Returns:
        True if the update was successful, False otherwise.
    """
    try:
        UserBase(name="dummy", email=new_email) 
    except Exception as e:
        print(f"Validation Error: Invalid email format for '{new_email}'. {e}")
        return False


    db = SessionLocal()
    try:
        user = db.query(User).filter(User.id == user_id).first()

        if user:
            user.email = new_email 
            db.commit()            
            print(f"Successfully updated email for user ID {user_id} to {new_email}")
            return True
        else:
            print(f"User with ID {user_id} not found for update.")
            return False

    except IntegrityError as e:
        db.rollback() 
        print(f"Error: Email '{new_email}' already exists for another user (IntegrityError). {e}")
        return False
    except Exception as e:
        db.rollback()
        print(f"An unexpected error occurred during update: {e}")
        return False
    finally:
        db.close()

if __name__ == "__main__":
    db = SessionLocal()
    alice = db.query(User).filter(User.email == "alice@example.com").first()
    bob = db.query(User).filter(User.email == "bob@example.com").first() 
    db.close()

    if alice:
        alice_id = alice.id
        print(f"Attempting to update email for user ID {alice_id} (Alice)...")
        update_successful = update_user_email(alice_id, "alice.new@example.com")

        if update_successful:
            db = SessionLocal()
            updated_alice = db.query(User).filter(User.id == alice_id).first()
            print(f"Verified updated email: {updated_alice.email}")
            db.close()

        print("\nAttempting to update with invalid email format...")
        update_user_email(alice_id, "not-an-email")

        bob_email = bob.email if bob else "bob@example.com"
        print(f"\nAttempting to update email for user ID {alice_id} to {bob_email} (duplicate)...")
        update_user_email(alice_id, bob_email)


    else:
        print("User with email alice@example.com not found. Cannot run update example.")