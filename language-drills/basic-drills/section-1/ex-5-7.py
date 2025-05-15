from contextlib import suppress

data = {"name": "Alice"}

with suppress(KeyError):
    age = data["age"]
    print(f"Age: {age}")

print("Continuing after potential KeyError.")