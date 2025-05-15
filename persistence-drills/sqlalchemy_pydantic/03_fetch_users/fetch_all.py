# sqlalchemy_pydantic/03_fetch_users/fetch_all.py

# --- DIAGNOSTIC ADDITION: Explicitly add parent directory to sys.path ---
import sys
import os

# Get the directory of the current script (03_fetch_users)
script_dir = os.path.dirname(os.path.abspath(__file__))
# Get the parent directory (sqlalchemy_pydantic)
parent_dir = os.path.dirname(script_dir)
# Add the parent directory to sys.path. This should be the directory containing shared.py.
sys.path.insert(0, parent_dir)
print(f"DEBUG: Added {parent_dir} to sys.path for import.")
# --- END DIAGNOSTIC ADDITION ---


from shared import SessionLocal, User, UserSchema
from typing import List

def get_users() -> List[UserSchema]:
    """
    Fetches all users from the database and returns them as a list of Pydantic models.
    """
    db = SessionLocal()
    try:
        # Query the database for all User objects
        users = db.query(User).all()

        # Convert the list of SQLAlchemy User objects to a list of Pydantic UserSchema models
        # UserSchema(user) works because from_attributes = True (or orm_mode = True) is set in UserSchema
        # Use model_validate in Pydantic v2+, from_orm in V1
        return [UserSchema.model_validate(user) for user in users]

    except Exception as e:
        print(f"Error fetching users: {e}")
        return [] # Return an empty list on error
    finally:
        db.close()


if __name__ == "__main__":
    # Make sure you have inserted some users first (run 02_insert_user/insert.py)

    all_users = get_users()

    if all_users:
        print("\n--- All Users in DB ---")
        # Assuming you updated Pydantic Config to use from_attributes=True
        # Use model_dump_json in Pydantic v2+, json() in V1
        # import json # Need to import json if you want to dump as JSON
        # for user_schema in all_users:
        #     print(json.dumps(user_schema.model_dump(), indent=2))
        # Or print attributes directly:
        for user_schema in all_users:
             print(f"ID: {user_schema.id}, Name: {user_schema.name}, Email: {user_schema.email}, Created At: {user_schema.created_at}")

        print("-----------------------")
    else:
        print("\nNo users found in the database.")