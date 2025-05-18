import sys
import os

script_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(script_dir)
sys.path.insert(0, parent_dir)
print(f"DEBUG: Added {parent_dir} to sys.path for import.")

from shared import SessionLocal, User, Post, UserWithPostsSchema
from typing import Optional
import json 
from sqlalchemy.orm import joinedload 

def get_user_with_posts(user_id: int) -> Optional[UserWithPostsSchema]:
    """
    Fetches a user and their associated posts, returns as a nested Pydantic model.
    """
    db = SessionLocal()
    try:
        user = db.query(User).options(joinedload(User.posts)).filter(User.id == user_id).first()

        if user:
            user_schema = UserWithPostsSchema.model_validate(user)
            return user_schema
        else:
            return None 

    except Exception as e:
        print(f"Error fetching user with posts: {e}")
        return None
    finally:
        db.close()

if __name__ == "__main__":
    db = SessionLocal()
    alice = db.query(User).filter(User.email == "alice.new@example.com").first()
    db.close()

    if alice:
        alice_id = alice.id
        fetched_user_with_posts = get_user_with_posts(alice_id)

        if fetched_user_with_posts:
            print(f"\nFetched User ID {alice_id} ({fetched_user_with_posts.name}) with Posts (as Pydantic model):")
            print(fetched_user_with_posts.model_dump_json(indent=4))
        else:
            print(f"\nUser with ID {alice_id} not found.")

    print("\nFetching user with no posts or non-existent user...")
    user_without_posts_id = 3 
    fetched_user_no_posts = get_user_with_posts(user_without_posts_id)

    if fetched_user_no_posts:
        print(f"\nFetched User ID {user_without_posts_id} with Posts:")
        print(fetched_user_no_posts.model_dump_json(indent=4))
    else:
        print(f"\nUser with ID {user_without_posts_id} not found.")