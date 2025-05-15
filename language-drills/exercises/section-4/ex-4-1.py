import itertools

id_generator = itertools.count(start=1) # Starts counting from 1

print("Generating IDs:")
print(next(id_generator)) # Output: 1
print(next(id_generator)) # Output: 2
print(next(id_generator)) # Output: 3

# Example: Generate first 5 user IDs
user_ids = [next(id_generator) for _ in range(5)]
print(f"Next 5 User IDs: {user_ids}") # Output: [4, 5, 6, 7, 8]