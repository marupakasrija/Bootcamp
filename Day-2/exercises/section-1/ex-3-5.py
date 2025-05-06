def process_data(name, *args, **kwargs):
    print(f"Name: {name}")
    print("Positional arguments (args):", args)
    print("Keyword arguments (kwargs):", kwargs)

process_data("Alice", 1, 2, 3, age=30, city="New York")
# Output:
# Name: Alice
# Positional arguments (args): (1, 2, 3)
# Keyword arguments (kwargs): {'age': 30, 'city': 'New York'}