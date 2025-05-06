from typing import Optional
from pydantic import BaseModel, Field

class User(BaseModel):
    name: str
    age: int
    email: Optional[str] = Field(None, description="User's email address")

if __name__ == "__main__":
    user = User(name="Alice", age=30, email="alice@example.com")
    print(user.schema_json(indent=2))