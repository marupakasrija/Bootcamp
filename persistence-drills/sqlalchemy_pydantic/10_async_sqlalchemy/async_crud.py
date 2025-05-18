import sys
import os
import asyncio
from typing import List, Optional
from shared import AsyncSessionLocal, User, UserCreate, UserSchema
from shared import create_async_tables
from sqlalchemy.exc import IntegrityError
from sqlalchemy import select 

script_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(script_dir)
sys.path.insert(0, parent_dir)
print(f"DEBUG: Added {parent_dir} to sys.path for import.")


async def create_async_user(user_data: UserCreate) -> Optional[UserSchema]:
    """
    Creates a new user asynchronously.
    """
    async with AsyncSessionLocal() as db:
        try:
            db_user = User(name=user_data.name, email=user_data.email)
            db.add(db_user)
            await db.commit() 
            await db.refresh(db_user) 

            print(f"Inserted async user with ID: {db_user.id}")
            return UserSchema.model_validate(db_user)

        except IntegrityError as e:
            await db.rollback() 
            print(f"Async error: User with email '{user_data.email}' already exists. {e}")
            return None
        except Exception as e:
            await db.rollback()
            print(f"An unexpected async error occurred: {e}")
            return None


async def get_async_users() -> List[UserSchema]:
    """
    Fetches all users asynchronously.
    """
    async with AsyncSessionLocal() as db:
        try:
            result = await db.execute(select(User))
            users = result.scalars().all()
            return [UserSchema.model_validate(user) for user in users]

        except Exception as e:
            print(f"Async error fetching users: {e}")
            return []

async def get_async_user_by_email(email: str) -> Optional[UserSchema]:
    """
    Fetches a single user by email asynchronously.
    """
    async with AsyncSessionLocal() as db:
        try:
            result = await db.execute(select(User).filter(User.email == email))
            user = result.scalars().first() 

            if user:
                return UserSchema.model_validate(user)
            else:
                return None

        except Exception as e:
            print(f"Async error fetching user by email: {e}")
            return None


async def main():
    await create_async_tables()
    print("-" * 20)

    print("\nAttempting to create async user...")
    user_in_1 = UserCreate(name="Async Alice", email="async.alice@example.com")
    created_user_1 = await create_async_user(user_in_1)
    if created_user_1:
        print(f"Created: {created_user_1.model_dump_json(indent=4)}") 

    user_in_2 = UserCreate(name="Async Bob", email="async.bob@example.com")
    created_user_2 = await create_async_user(user_in_2)
    if created_user_2:
        print(f"Created: {created_user_2.model_dump_json(indent=4)}") 

    user_in_3 = UserCreate(name="Async Alice Again", email="async.alice@example.com")
    await create_async_user(user_in_3)

    print("-" * 20)

    print("\nAttempting to fetch all async users...")
    all_async_users = await get_async_users()
    if all_async_users:
        print("Fetched async users:")
        for user in all_async_users:
            print(user.model_dump_json(indent=2)) 
    else:
        print("No async users found.")

    print("-" * 20)

    # Fetch user by email asynchronously
    print("\nAttempting to fetch 'async.bob@example.com'...")
    bob_user = await get_async_user_by_email("async.bob@example.com")
    if bob_user:
        print(f"Found async user: {bob_user.model_dump_json(indent=4)}") # V2
    else:
        print("Async user 'async.bob@example.com' not found.")

if __name__ == "__main__":
    asyncio.run(main())