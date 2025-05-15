from pydantic import BaseModel, validator

class User(BaseModel):
    name: str
    age: int

    @validator("name")
    def check_name_capitalization(cls, value):
        if not value[0].isupper():
            raise ValueError("Name must start with a capital letter")
        return value

if __name__ == "__main__":
    valid_data = {"name": "Alice", "age": 30}
    user_valid = User(**valid_data)
    print(user_valid)

    invalid_data = {"name": "alice", "age": 25}
    try:
        user_invalid = User(**invalid_data)
    except Exception as e:
        print(f"Validation error: {e}")