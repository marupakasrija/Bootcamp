user = {"name": "Alice"}

# Using .get()
age = user.get("age")
print(f"Age (using get): {age}")  # Returns None as "age" key doesn't exist
age = user.get("age", 25)
print(f"Age (using get with default): {age}")  # Returns the default value 25

# Using .setdefault()
city = user.setdefault("city", "New York")
print(f"User (after setdefault): {user}, City: {city}")  # Adds "city": "New York" and returns "New York"
country = user.setdefault("name", "Bob")
print(f"User (after attempting setdefault on existing key): {user}, Country: {country}") # Returns existing value "Alice"