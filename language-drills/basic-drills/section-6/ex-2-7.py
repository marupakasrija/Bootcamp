from pydantic import BaseModel

class User(BaseModel):
    name: str
    age: int

if __name__ == "__main__":
    user = User(name="Alice", age=30)
    user_dict = user.dict()
    user_json = user.json()
    print(f"Dictionary: {user_dict}")
    print(f"JSON: {user_json}")