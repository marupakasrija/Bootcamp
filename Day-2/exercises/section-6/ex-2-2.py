from pydantic import BaseModel, ValidationError

class User(BaseModel):
    name: str
    age: int

if __name__ == "__main__":
    invalid_data = {"name": "Bob", "age": "not a number"}
    try:
        user = User(**invalid_data)
    except ValidationError as e:
        print(f"Validation error: {e}")