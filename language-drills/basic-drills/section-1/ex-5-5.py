class InvalidAgeError(Exception):
    """Custom exception raised when age is invalid."""
    pass

def set_age(age):
    if age < 0:
        raise InvalidAgeError("Age cannot be negative.")
    else:
        print(f"Age set to: {age}")

try:
    set_age(30)
    set_age(-5)
except InvalidAgeError as e:
    print(f"Error: {e}")