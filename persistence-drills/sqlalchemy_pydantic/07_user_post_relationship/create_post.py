# sqlalchemy_pydantic/07_user_post_relationship/create_post.py

# --- DIAGNOSTIC ADDITION: Explicitly add parent directory to sys.path ---
import sys
import os

# Get the directory of the current script (07_user_post_relationship)
script_dir = os.path.dirname(os.path.abspath(__file__))
# Get the parent directory (sqlalchemy_pydantic)
parent_dir = os.path.dirname(script_dir)
# Add the parent directory to sys.path. This should be the directory containing shared.py.
sys.path.insert(0, parent_dir)
print(f"DEBUG: Added {parent_dir} to sys.path for import.")
# --- END DIAGNOSTIC ADDITION ---


# This exercise is primarily about adding the Post model and relationship
# definitions in shared.py. This script demonstrates creating posts
# and linking them to users.

# Make sure you have updated shared.py with the Post model
# And run 01_basic_model/create_tables.py again AFTER updating shared.py

from shared import SessionLocal, User, Post, PostCreate

def create_post(post_data: PostCreate):
    """
    Creates a new post in the database.

    Args:
        post_data: A Pydantic PostCreate model.
    """
    db = SessionLocal()
    try:
        # Optional: Verify the author exists (ForeignKey constraint handles this in DB too)
        author = db.query(User).filter(User.id == post_data.author_id).first()
        if not author:
            print(f"Error: Author with ID {post_data.author_id} not found. Post not created.")
            return None

        # Create SQLAlchemy Post instance from Pydantic data
        db_post = Post(
            title=post_data.title,
            content=post_data.content,
            author_id=post_data.author_id # Link via foreign key
        )

        db.add(db_post)
        db.commit()
        db.refresh(db_post) # Get the database-assigned ID

        print(f"Inserted post with ID: {db_post.id}, Title: '{db_post.title}' by User ID: {db_post.author_id}")
        return db_post

    except Exception as e:
        db.rollback()
        print(f"An unexpected error occurred creating post: {e}")
        return None
    finally:
        db.close()

if __name__ == "__main__":
    # Make sure you have users in the database (run 02_insert_user/insert.py)
    # Make sure you have updated shared.py with the Post model and run create_tables.py first!

    db = SessionLocal()
    # Fetch Alice and Bob to get their IDs
    # Ensure shared.py includes the User model and SessionLocal
    try:
        alice = db.query(User).filter(User.email == "alice.new@example.com").first() # Use potentially updated email
        bob = db.query(User).filter(User.email == "bob@example.com").first()
    finally:
        db.close() # Close session after fetching IDs


    if alice:
        alice_id = alice.id
        print(f"\nAdding post for user ID {alice_id} (Alice)...")
        post_data_1 = PostCreate(title="Alice's First Post", content="Content...", author_id=alice_id)
        create_post(post_data_1)

        print(f"\nAdding another post for user ID {alice_id} (Alice)...")
        post_data_2 = PostCreate(title="Alice's Second Post", content="More content...", author_id=alice_id)
        create_post(post_data_2)
    else:
         print("Alice user not found. Cannot create posts for Alice. Run 02_insert_user/insert.py")


    if bob:
        bob_id = bob.id
        print(f"\nAdding post for user ID {bob_id} (Bob)...")
        post_data_3 = PostCreate(title="Bob's Blog", content="Hello world!", author_id=bob_id)
        create_post(post_data_3)
    else:
         print("Bob user not found. Cannot create posts for Bob. Run 02_insert_user/insert.py")


    # Attempt to create a post for a non-existent user (will likely fail due to FK constraint if active)
    print("\nAttempting to create post for non-existent user (ID 999)...")
    post_data_invalid = PostCreate(title="Post by Unknown", content="...", author_id=999)
    create_post(post_data_invalid)