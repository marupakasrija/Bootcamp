
import sys
import os

script_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(script_dir)
sys.path.insert(0, parent_dir)
print(f"DEBUG: Added {parent_dir} to sys.path for import.")


from shared import SessionLocal, User

def delete_user_by_id(user_id: int) -> bool:
    """
    Deletes a user by their ID.

    Args:
        user_id: The ID of the user to delete.

    Returns:
        True if the user was found and deleted, False otherwise.
    """
    db = SessionLocal()
    try:
        user = db.query(User).filter(User.id == user_id).first()

        if user:
            db.delete(user)
            db.commit()     
            print(f"Successfully deleted user with ID {user_id}")
            return True
        else:
            print(f"User with ID {user_id} not found for deletion.")
            return False

    except Exception as e:
        db.rollback() 
        print(f"An unexpected error occurred during deletion: {e}")
        return False
    finally:
        db.close()

if __name__ == "__main__":
    db = SessionLocal()
    bob = db.query(User).filter(User.email == "bob@example.com").first()
    bob_id = bob.id if bob else None
    db.close()

    if bob_id is not None:
        print(f"Attempting to delete user with ID {bob_id} (Bob)...")
        delete_successful = delete_user_by_id(bob_id)

        if delete_successful:
            db = SessionLocal()
            deleted_user = db.query(User).filter(User.id == bob_id).first()
            if deleted_user is None:
                 print(f"Verification successful: User with ID {bob_id} is no longer in the database.")
            else:
                 print(f"Verification failed: User with ID {bob_id} still found.")
            db.close()

    else:
        print("User with email bob@example.com not found. Cannot run delete example.")

    print("\nAttempting to delete a non-existent user (ID 999)...")
    delete_user_by_id(999)