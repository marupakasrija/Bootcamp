# sqlalchemy_pydantic/04_filtering/filter_by_email.py

# --- DIAGNOSTIC ADDITION: Explicitly add parent directory to sys.path ---
import sys
import os

# Get the directory of the current script (04_filtering)
script_dir = os.path.dirname(os.path.abspath(__file__))
# Get the parent directory (sqlalchemy_pydantic)
parent_dir = os.path.dirname(script_dir)
# Add the parent directory to sys.path. This should be the directory containing shared.py.
sys.path.insert(0, parent_dir)
print(f"DEBUG: Added {parent_dir} to sys.path for import.")
# --- END DIAGNOSTIC ADDITION ---


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
        # Query the database, filter by email, and get the first result
        # .filter() uses standard Python comparison operators which SQLAlchemy translates to SQL
        user = db.query(User).filter(User.email == email).first()

        if user:
            # Convert SQLAlchemy model to Pydantic model
            # Use model_validate in Pydantic v2+, from_orm in V1
            return UserSchema.model_validate(user)
        else:
            return None # User not found

    except Exception as e:
        print(f"Error fetching user by email: {e}")
        return None
    finally:
        db.close()

if __name__ == "__main__":
    # Make sure you have inserted users first (run 02_insert_user/insert.py)

    # Search for an existing user
    existing_email = "alice@example.com" # Use an email you know exists
    found_user = get_user_by_email(existing_email)

    if found_user:
        print(f"\nFound user with email {existing_email}:")
        print(f"ID: {found_user.id}, Name: {found_user.name}, Email: {found_user.email}, Created At: {found_user.created_at}")
    else:
        print(f"\nUser with email {existing_email} not found.")

    # Search for a non-existent user
    non_existent_email = "nonexistent@example.com"
    not_found_user = get_user_by_email(non_existent_email)

    if not_found_user:
        print(f"\nFound user with email {non_existent_email}:")
        print(f"ID: {not_found_user.id}, Name: {not_found_user.name}, Email: {not_found_user.email}")
    else:
        print(f"\nUser with email {non_existent_email} not found.")