from collections import defaultdict

# Create a defaultdict where missing keys return "N/A"
na_dict = defaultdict(lambda: "N/A")

na_dict['existing_key'] = "Some Value"

print(f"Value for 'existing_key': {na_dict['existing_key']}")
print(f"Value for 'missing_key1': {na_dict['missing_key1']}")
print(f"Value for 'missing_key2': {na_dict['missing_key2']}")
print(f"Current dict state: {dict(na_dict)}") # Note: accessing missing keys adds them

# Expected Output:
# Value for 'existing_key': Some Value
# Value for 'missing_key1': N/A
# Value for 'missing_key2': N/A
# Current dict state: {'existing_key': 'Some Value', 'missing_key1': 'N/A', 'missing_key2': 'N/A'}