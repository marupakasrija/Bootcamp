# sqlalchemy_pydantic/08_nested_response/fetch_user_with_posts.py

# --- DIAGNOSTIC ADDITION: Explicitly add parent directory to sys.path ---
import sys
import os

# Get the directory of the current script (08_nested_response)
script_dir = os.path.dirname(os.path.abspath(__file__))
# Get the parent directory (sqlalchemy_pydantic)
parent_dir = os.path.dirname(script_dir)
# Add the parent directory to sys.path. This should be the directory containing shared.py.
sys.path.insert(0, parent_dir)
print(f"DEBUG: Added {parent_dir} to sys.path for import.")
# --- END DIAGNOSTIC ADDITION ---


# This exercise demonstrates fetching a user and their related posts
# and returning it as a nested Pydantic model.

# Make sure you have updated shared.py with the Post model and User/Post relationships
# Make sure you have run 01_basic_model/create_tables.py after updating shared.py
# Make sure you have created users and posts (run 02_insert_user/insert.py and 07_user_post_relationship/create_post.py)

from shared import SessionLocal, User, Post, UserWithPostsSchema
from typing import Optional
import json # To print the nested structure nicely
from sqlalchemy.orm import joinedload # Optional: for eager loading

def get_user_with_posts(user_id: int) -> Optional[UserWithPostsSchema]:
    """
    Fetches a user and their associated posts, returns as a nested Pydantic model.
    """
    db = SessionLocal()
    try:
        # Query for the user. SQLAlchemy loads relationships lazily by default.
        # To eager load the posts in the same query, use .options(joinedload(User.posts))
        # For simplicity here, we'll rely on lazy loading when accessing user.posts later.
        # Use joinedload for a single efficient query:
        user = db.query(User).options(joinedload(User.posts)).filter(User.id == user_id).first()

        if user:
            # Convert the SQLAlchemy User object to the UserWithPostsSchema Pydantic model
            # Because from_attributes=True is set and the relationship 'posts' is defined,
            # Pydantic will automatically load the associated Post objects
            # and convert them to PostSchema models.
            # Use model_validate in Pydantic v2+, from_orm in V1
            user_schema = UserWithPostsSchema.model_validate(user)
            return user_schema
        else:
            return None # User not found

    except Exception as e:
        print(f"Error fetching user with posts: {e}")
        return None
    finally:
        db.close()

if __name__ == "__main__":
    # Make sure prerequisite scripts have been run (users and posts created)

    # Fetch and display user with posts (e.g., Alice)
    # You'll need Alice's ID - fetch it first or know it from previous inserts
    db = SessionLocal()
    # Assuming Alice's email was updated to alice.new@example.com in Drill 5
    alice = db.query(User).filter(User.email == "alice.new@example.com").first()
    db.close()

    if alice:
        alice_id = alice.id
        fetched_user_with_posts = get_user_with_posts(alice_id)

        if fetched_user_with_posts:
            print(f"\nFetched User ID {alice_id} ({fetched_user_with_posts.name}) with Posts (as Pydantic model):")
            # Pydantic model can be converted to JSON easily
            # Use model_dump_json in Pydantic v2+, json() in V1
            print(fetched_user_with_posts.model_dump_json(indent=4))
        else:
            print(f"\nUser with ID {alice_id} not found.")

    # Fetch a user with no posts (or non-existent user)
    print("\nFetching user with no posts or non-existent user...")
    # Let's try user ID 3 (assuming Charlie or a new ID without posts)
    user_without_posts_id = 3 # Adjust if needed based on your data
    fetched_user_no_posts = get_user_with_posts(user_without_posts_id)

    if fetched_user_no_posts:
        print(f"\nFetched User ID {user_without_posts_id} with Posts:")
        print(fetched_user_no_posts.model_dump_json(indent=4))
    else:
        print(f"\nUser with ID {user_without_posts_id} not found.")