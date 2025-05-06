person = {"name": "Bob", "age": 30}

# Iterating through keys
print("Keys:")
for key in person:
    print(key)

# Iterating through values
print("\nValues:")
for value in person.values():
    print(value)

# Iterating through key-value pairs
print("\nKey-Value Pairs:")
for key, value in person.items():
    print(f"{key}: {value}")