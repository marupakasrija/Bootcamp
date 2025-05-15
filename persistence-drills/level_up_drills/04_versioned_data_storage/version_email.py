# level_up_drills/04_versioned_data_storage/version_email.py

# --- DIAGNOSTIC ADDITION: Explicitly add parent directory to sys.path ---
# This is a workaround for environments where python -m doesn't automatically
# add the package root (the directory containing shared.py for this package)
# to sys.path correctly.
import sys
import os

# Get the directory of the current script (04_versioned_data_storage)
script_dir = os.path.dirname(os.path.abspath(__file__))
# Get the parent directory (level_up_drills)
parent_dir = os.path.dirname(script_dir)
# Add the parent directory to sys.path. This should be the directory containing shared.py for this package.
sys.path.insert(0, parent_dir)
print(f"DEBUG: Added {parent_dir} to sys.path for import.")
# --- END DIAGNOSTIC ADDITION ---


# Import necessary components and MODELS from shared.py
from shared import SessionLocal, Base, engine, create_tables, User, UserEmailHistory # Import User and UserEmailHistory

from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, func # Still needed for types if defining elsewhere or for context
from sqlalchemy.orm import Session # For type hinting
import datetime
from typing import List, Optional


# --- REMOVE THE HISTORY MODEL DEFINITION FROM HERE ---
# The definition of class UserEmailHistory(Base): ... should be ONLY in shared.py.
# Delete that entire class definition block from THIS file.


# Ensure tables exist (run once)
# ... (comments on running create_tables) ...


# --- Logic to Update Email and Version ---
def update_user_email_with_versioning(user_id: int, new_email: str) -> Optional[User]:
    """
    Updates a user's email and logs the change in the history table, within a transaction.
    """
    db = SessionLocal() # Use the appropriate SessionLocal
    try:
        # Start a transaction
        # SQLAlchemy sessions automatically manage transactions.
        # Call db.begin() explicitly if you need nested transactions or more control,
        # but for a single unit of work, commit/rollback is sufficient.

        # 1. Fetch the user
        user = db.query(User).filter(User.id == user_id).first()

        if not user:
            print(f"User with ID {user_id} not found.")
            db.rollback() # Rollback any implicit transaction started
            return None

        # Check if the email is actually changing
        if user.email == new_email:
            print(f"Email for user ID {user_id} is already {new_email}. No change needed.")
            db.rollback() # Rollback if no change
            return user # Return current user

        # 2. Create a history record for the NEW email
        history_entry = UserEmailHistory( # Use the imported model
            user_id=user.id,
            email=new_email,
            # changed_at defaults to now() via server_default
            # old_email=user.email # If storing old email
        )
        db.add(history_entry)
        # The history_entry object doesn't have its ID yet until it's flushed/committed.
        # If you needed the history ID immediately (e.g., to store in user.current_email_version_id),
        # you'd need to flush the session: db.flush()
        # In this design, we just update the user's email directly.

        # 3. Update the user's current email
        user.email = new_email
        # If you stored current_email_version_id in the User table:
        # db.flush() # Flush to get the history_entry ID
        # user.current_email_version_id = history_entry.id

        # 4. Commit the transaction (both history insert and user update happen together)
        db.commit()

        # Refresh the user object to get the latest state from the database
        # (e.g., if current_email_version_id was updated)
        db.refresh(user)

        print(f"Successfully updated email for user ID {user_id} to {new_email} and logged history.")
        return user

    except Exception as e:
        db.rollback() # Rollback the entire transaction on error
        print(f"Error updating email for user ID {user_id} (transaction rolled back): {e}")
        return None
    finally:
        db.close()


# --- Queries for Version History ---

def get_user_email_history(user_id: int) -> List[UserEmailHistory]:
    """Fetches all email history records for a user."""
    db = SessionLocal()
    try:
        # Query the history table, filter by user_id, order by timestamp
        history = db.query(UserEmailHistory)\
                    .filter(UserEmailHistory.user_id == user_id)\
                    .order_by(UserEmailHistory.changed_at.desc())\
                    .all()
        return history
    except Exception as e:
        print(f"Error fetching history for user ID {user_id}: {e}")
        return []
    finally:
        db.close()

# To get the latest email, you would just query the User table:
# def get_user_current_email(user_id: int) -> Optional[str]:
#     db = SessionLocal()
#     try:
#         user = db.query(User.email).filter(User.id == user_id).first()
#         return user[0] if user else None
#     finally:
#         db.close()


if __name__ == "__main__":
    # Ensure User and UserEmailHistory tables exist
    # Add UserEmailHistory model to your shared.py Base.metadata
    # and run create_tables() once before running this script.
    # You also need a user to exist (e.g., create Alice via 02_insert_user/insert.py from practice drills)

    # --- Example Usage ---
    db = SessionLocal()
    # Fetch Alice's ID (assuming she exists)
    # Use the email from previous steps if it changed (e.g. alice.new@example.com)
    alice = db.query(User).filter(User.email.like("alice%example.com")).first() # Flexible search
    alice_id = alice.id if alice else None
    alice_current_email = alice.email if alice else None
    db.close()

    if alice_id is not None:
        print(f"Initial email for user ID {alice_id} (Alice): {alice_current_email}")

        # 1. Update email for the first time
        new_email_1 = "alice.updated1@example.com"
        print(f"\nUpdating email for user ID {alice_id} to {new_email_1}...")
        update_user_email_with_versioning(alice_id, new_email_1)

        # 2. Update email again
        new_email_2 = "alice.updated2@example.com"
        print(f"\nUpdating email for user ID {alice_id} to {new_email_2}...")
        update_user_email_with_versioning(alice_id, new_email_2)

        # 3. Attempt to update to the same email (should do nothing)
        print(f"\nAttempting to update email for user ID {alice_id} to {new_email_2} again...")
        update_user_email_with_versioning(alice_id, new_email_2)

        # 4. Attempt to update email for a non-existent user
        print("\nAttempting to update email for non-existent user (ID 999)...")
        update_user_email_with_versioning(999, "noone@example.com")


        # --- Fetch and display history ---
        print(f"\nFetching email history for user ID {alice_id}:")
        history_records = get_user_email_history(alice_id)

        if history_records:
            for record in history_records:
                print(f"- Email: {record.email}, Changed At: {record.changed_at}")
        else:
            print("No history found.")

    else:
        print("Alice user not found. Cannot run versioning example. Please ensure a user exists.")