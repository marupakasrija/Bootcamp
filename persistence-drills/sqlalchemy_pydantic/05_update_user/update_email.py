# sqlalchemy_pydantic/05_update_user/update_email.py

# --- DIAGNOSTIC ADDITION: Explicitly add parent directory to sys.path ---
import sys
import os

# Get the directory of the current script (05_update_user)
script_dir = os.path.dirname(os.path.abspath(__file__))
# Get the parent directory (sqlalchemy_pydantic)
parent_dir = os.path.dirname(script_dir)
# Add the parent directory to sys.path. This should be the directory containing shared.py.
sys.path.insert(0, parent_dir)
print(f"DEBUG: Added {parent_dir} to sys.path for import.")
# --- END DIAGNOSTIC ADDITION ---


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
    # Basic Pydantic-like validation for the new email format
    # (You could use a Pydantic model here too if validating multiple fields)
    try:
        UserBase(name="dummy", email=new_email) # Use UserBase for email format validation
    except Exception as e:
        print(f"Validation Error: Invalid email format for '{new_email}'. {e}")
        return False


    db = SessionLocal()
    try:
        # Find the user by ID
        user = db.query(User).filter(User.id == user_id).first()

        if user:
            user.email = new_email # Update the attribute on the SQLAlchemy object
            db.commit()            # Commit the change
            # db.refresh(user) # Optional: refresh if you needed database-generated values after update
            print(f"Successfully updated email for user ID {user_id} to {new_email}")
            return True
        else:
            print(f"User with ID {user_id} not found for update.")
            return False

    except IntegrityError as e:
        db.rollback() # Rollback if the new email conflicts with an existing one (UNIQUE constraint)
        print(f"Error: Email '{new_email}' already exists for another user (IntegrityError). {e}")
        return False
    except Exception as e:
        db.rollback()
        print(f"An unexpected error occurred during update: {e}")
        return False
    finally:
        db.close()

if __name__ == "__main__":
    # Make sure you have inserted users first (run 02_insert_user/insert.py)
    # You'll need the ID of a user to update.
    # Let's fetch Alice's ID first (assuming insert_user.py was run)
    db = SessionLocal()
    alice = db.query(User).filter(User.email == "alice@example.com").first()
    bob = db.query(User).filter(User.email == "bob@example.com").first() # To get bob's email for duplicate test
    db.close()

    if alice:
        alice_id = alice.id
        print(f"Attempting to update email for user ID {alice_id} (Alice)...")
        update_successful = update_user_email(alice_id, "alice.new@example.com")

        if update_successful:
            # Verify the update by fetching again
            db = SessionLocal()
            updated_alice = db.query(User).filter(User.id == alice_id).first()
            print(f"Verified updated email: {updated_alice.email}")
            db.close()

        # Attempt to update with an invalid email format
        print("\nAttempting to update with invalid email format...")
        update_user_email(alice_id, "not-an-email")

        # Attempt to update to an email that already exists (e.g., Bob's email)
        bob_email = bob.email if bob else "bob@example.com"
        print(f"\nAttempting to update email for user ID {alice_id} to {bob_email} (duplicate)...")
        update_user_email(alice_id, bob_email)


    else:
        print("User with email alice@example.com not found. Cannot run update example.")