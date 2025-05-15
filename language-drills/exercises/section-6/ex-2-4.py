from pydantic import BaseModel, Field
from typing import Annotated

class User(BaseModel):
    name: Annotated[str, Field(min_length=3)]
    age: Annotated[int, Field(gt=0)]

if __name__ == "__main__":
    valid_data = {"name": "Alice", "age": 30}
    user_valid = User(**valid_data)
    print(user_valid)

    invalid_name_data = {"name": "Al", "age": 25}
    try:
        user_invalid_name = User(**invalid_name_data)
    except Exception as e:
        print(f"Validation error (name): {e}")

    invalid_age_data = {"name": "Bob", "age": 0}
    try:
        user_invalid_age = User(**invalid_age_data)
    except Exception as e:
        print(f"Validation error (age): {e}")