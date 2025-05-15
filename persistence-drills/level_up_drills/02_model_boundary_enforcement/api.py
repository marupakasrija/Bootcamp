# level_up_drills/02_model_boundary_enforcement/api.py

# --- DIAGNOSTIC ADDITION: Explicitly add parent directory to sys.path ---
# This is a workaround for environments where python -m doesn't automatically
# add the package root (the directory containing shared.py for this package)
# to sys.path correctly.
import sys
import os

# Get the directory of the current script (02_model_boundary_enforcement)
script_dir = os.path.dirname(os.path.abspath(__file__))
# Get the parent directory (level_up_drills)
parent_dir = os.path.dirname(script_dir)
# Add the parent directory to sys.path. This should be the directory containing shared.py for this package.
sys.path.insert(0, parent_dir)
print(f"DEBUG: Added {parent_dir} to sys.path for import.")
# --- END DIAGNOSTIC ADDITION ---


# This layer interacts with request/response data (Pydantic models)
# and calls the service layer. It should not pass SQLAlchemy models outside.

# In a real web framework (like FastAPI), this would use request/response objects.
# Here, we simulate it with functions.

# Import Pydantic schemas and SQLAlchemy User from shared.py
# This import should now work if shared.py is in the directory added to sys.path
from shared import SessionLocal, User, UserBase, UserCreate, UserSchema

# Import the service layer - assuming services.py is in the same directory
from . import services

from typing import List, Optional
# Simulate framework dependency injection for the database session
from contextlib import contextmanager

@contextmanager
def get_db_session():
    """Helper to get a database session for this simulation."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def get_user_endpoint(user_id: int) -> Optional[UserSchema]:
    """Simulates an API endpoint to get a user."""
    with get_db_session() as db:
        db_user = services.get_user_from_db(db, user_id)
        if db_user:
            # Convert SQLAlchemy model to Pydantic model for the response
            # Use model_validate in Pydantic v2+, from_orm in V1
            return UserSchema.model_validate(db_user)
        return None # User not found

def create_user_endpoint(user_data: UserCreate) -> UserSchema:
    """Simulates an API endpoint to create a user."""
    # user_data is already a validated Pydantic model from the "request"
    with get_db_session() as db:
        # Convert Pydantic input model to SQLAlchemy model for the service layer
        db_user = User(name=user_data.name, email=user_data.email)
        # Call the service layer
        created_user = services.create_user_in_db(db, db_user)
        # Convert the resulting SQLAlchemy model to Pydantic model for the response
        # Use model_validate in Pydantic v2+, from_orm in V1
        return UserSchema.model_validate(created_user)

def update_user_email_endpoint(user_id: int, user_update: UserBase) -> Optional[UserSchema]:
    """Simulates an API endpoint to update a user's email."""
    # user_update contains the validated data for the update
    with get_db_session() as db:
        db_user = services.get_user_from_db(db, user_id)
        if db_user:
            # Update the SQLAlchemy model attributes using data from Pydantic model
            updated_user_db = services.update_user_email_in_db(db, db_user, new_email=user_update.email)
            # Convert the resulting SQLAlchemy model to Pydantic model for the response
            # Use model_validate in Pydantic v2+, from_orm in V1
            return UserSchema.model_validate(updated_user_db)
        return None # User not found


if __name__ == "__main__":
    print("Demonstrating Model Boundary Enforcement:")

    # Simulate creating a user via the API layer
    user_in = UserCreate(name="Boundary Bob", email="boundary.bob@example.com")
    print("\nCreating user via API endpoint...")
    created_user_schema = create_user_endpoint(user_in)
    # Use model_dump_json in Pydantic v2+, json() in V1
    if created_user_schema:
         print(f"API received (Pydantic): {created_user_schema.model_dump_json(indent=2)}")
    else:
         print("Failed to create user.")


    # Simulate fetching a user via the API layer
    print("\nFetching user via API endpoint...")
    # Need the ID - fetch it first using a service function or know it
    # Use a new session for this separate operation
    with get_db_session() as db:
         bob_db = services.get_user_from_db(db, created_user_schema.id if created_user_schema else -1) # Use created ID or -1 if failed
         bob_id = bob_db.id if bob_db else None

    if bob_id is not None:
         fetched_user_schema = get_user_endpoint(bob_id)
         if fetched_user_schema:
              print(f"API received (Pydantic): {fetched_user_schema.model_dump_json(indent=2)}")

         # Simulate updating email via API layer
         update_data = UserBase(name="Ignored Name", email="bob.updated@example.com") # Name is ignored by update logic
         print("\nUpdating user email via API endpoint...")
         updated_user_schema = update_user_email_endpoint(bob_id, update_data)
         if updated_user_schema:
              print(f"API received (Pydantic): {updated_user_schema.model_dump_json(indent=2)}")
    else:
        print("Failed to find user 'Boundary Bob' to demonstrate fetch/update.")