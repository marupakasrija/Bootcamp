import sys
import os

script_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(script_dir)
sys.path.insert(0, parent_dir)
print(f"DEBUG: Added {parent_dir} to sys.path for import.")

from shared import SessionLocal, User, UserSchema
from typing import Optional

def get_user_by_email(email: str) -> Optional[UserSchema]:
    """
    Fetches a single user by email.

    Args:
        email: The email address to search for.

    Returns:
        A Pydantic UserSchema model if found, otherwise None.
    """
    db = SessionLocal()
    try:
        user = db.query(User).filter(User.email == email).first()

        if user:
            return UserSchema.model_validate(user)
        else:
            return None 

    except Exception as e:
        print(f"Error fetching user by email: {e}")
        return None
    finally:
        db.close()

if __name__ == "__main__":

    existing_email = "alice@example.com"
    found_user = get_user_by_email(existing_email)

    if found_user:
        print(f"\nFound user with email {existing_email}:")
        print(f"ID: {found_user.id}, Name: {found_user.name}, Email: {found_user.email}, Created At: {found_user.created_at}")
    else:
        print(f"\nUser with email {existing_email} not found.")

    non_existent_email = "nonexistent@example.com"
    not_found_user = get_user_by_email(non_existent_email)

    if not_found_user:
        print(f"\nFound user with email {non_existent_email}:")
        print(f"ID: {not_found_user.id}, Name: {not_found_user.name}, Email: {not_found_user.email}")
    else:
        print(f"\nUser with email {non_existent_email} not found.")