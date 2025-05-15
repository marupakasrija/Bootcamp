import itertools

list_of_nones = list(itertools.repeat(None, 10))
print(f"List of ten Nones: {list_of_nones}")
print(f"Length of the list: {len(list_of_nones)}")

# Output:
# List of ten Nones: [None, None, None, None, None, None, None, None, None, None]
# Length of the list: 10