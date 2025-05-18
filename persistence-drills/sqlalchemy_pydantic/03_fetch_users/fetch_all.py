import sys
import os

script_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(script_dir)
sys.path.insert(0, parent_dir)
print(f"DEBUG: Added {parent_dir} to sys.path for import.")


from shared import SessionLocal, User, UserSchema
from typing import List

def get_users() -> List[UserSchema]:
    """
    Fetches all users from the database and returns them as a list of Pydantic models.
    """
    db = SessionLocal()
    try:
        users = db.query(User).all()
        return [UserSchema.model_validate(user) for user in users]

    except Exception as e:
        print(f"Error fetching users: {e}")
        return [] 
    finally:
        db.close()


if __name__ == "__main__":

    all_users = get_users()

    if all_users:
        print("\n--- All Users in DB ---")
        for user_schema in all_users:
             print(f"ID: {user_schema.id}, Name: {user_schema.name}, Email: {user_schema.email}, Created At: {user_schema.created_at}")

        print("-----------------------")
    else:
        print("\nNo users found in the database.")