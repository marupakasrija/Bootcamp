from typing import Optional
from pydantic import BaseModel, Field

class User(BaseModel):
    id: int = Field(..., alias="user_id")
    name: str
    age: int

if __name__ == "__main__":
    user_data = {"user_id": 123, "name": "Alice", "age": 30}
    user = User(**user_data)
    print(user)
    print(user.dict(by_alias=True))