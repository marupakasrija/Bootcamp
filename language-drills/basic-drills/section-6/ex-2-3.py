from pydantic import BaseModel

class Profile(BaseModel):
    country: str
    city: str

class User(BaseModel):
    name: str
    age: int
    profile: Profile

if __name__ == "__main__":
    user_data = {
        "name": "Alice",
        "age": 30,
        "profile": {"country": "USA", "city": "New York"},
    }
    user = User(**user_data)
    print(user)