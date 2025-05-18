import sys
import os

script_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(script_dir)
sys.path.insert(0, parent_dir)
print(f"DEBUG: Added {parent_dir} to sys.path for import.")

from shared import SessionLocal, User, Post, PostCreate

def create_post(post_data: PostCreate):
    """
    Creates a new post in the database.

    Args:
        post_data: A Pydantic PostCreate model.
    """
    db = SessionLocal()
    try:
        author = db.query(User).filter(User.id == post_data.author_id).first()
        if not author:
            print(f"Error: Author with ID {post_data.author_id} not found. Post not created.")
            return None

        db_post = Post(
            title=post_data.title,
            content=post_data.content,
            author_id=post_data.author_id 
        )

        db.add(db_post)
        db.commit()
        db.refresh(db_post) 

        print(f"Inserted post with ID: {db_post.id}, Title: '{db_post.title}' by User ID: {db_post.author_id}")
        return db_post

    except Exception as e:
        db.rollback()
        print(f"An unexpected error occurred creating post: {e}")
        return None
    finally:
        db.close()

if __name__ == "__main__":
    db = SessionLocal()
    try:
        alice = db.query(User).filter(User.email == "alice.new@example.com").first()
        bob = db.query(User).filter(User.email == "bob@example.com").first()
    finally:
        db.close() 


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


    print("\nAttempting to create post for non-existent user (ID 999)...")
    post_data_invalid = PostCreate(title="Post by Unknown", content="...", author_id=999)
    create_post(post_data_invalid)