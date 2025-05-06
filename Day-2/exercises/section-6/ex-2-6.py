from pydantic import BaseModel

class User(BaseModel):
    name: str
    age: int

if __name__ == "__main__":
    user_data = {"name": "Alice", "age": "42"}
    user = User(**user_data)
    print(f"Age as string passed: {user_data['age']}")
    print(f"Age after pydantic conversion: {user.age}, type: {type(user.age)}")