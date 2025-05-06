pairs = [(1, 2), (3, 4), (5, 6)]

print("Iterating through pairs:")
for x, y in pairs:
    print(f"x: {x}, y: {y}")

# Unpacking tuples of different lengths will result in an error
try:
    mixed_pairs = [(1, 2), (3, 4, 5)]
    for a, b in mixed_pairs:
        print(f"a: {a}, b: {b}")
except ValueError as e:
    print(f"\nError: {e}")