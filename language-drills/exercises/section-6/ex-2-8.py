from typing import Optional
from pydantic import BaseModel

class User(BaseModel):
    name: str
    age: int
    email: Optional[str] = None

if __name__ == "__main__":
    user1 = User(name="Alice", age=30)
    user2 = User(name="Bob", age=25, email="bob@example.com")
    print(user1)
    print(user2)