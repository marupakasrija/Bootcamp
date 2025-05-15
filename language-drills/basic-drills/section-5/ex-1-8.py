from collections import defaultdict

# 1. defaultdict(dict): a dictionary where each missing key defaults to an empty standard dictionary.
config = defaultdict(dict)
config['user']['name'] = "Alice"
config['user']['email'] = "alice@example.com"
config['system']['theme'] = "dark"

print("defaultdict(dict) example:")
print(dict(config))
print(f"User name: {config['user']['name']}")
# print(config['server']['port']) # This would create config['server'] = {} and then raise KeyError for 'port'

# 2. defaultdict(defaultdict(int)): a dictionary where missing keys default to
#    another defaultdict, which in turn defaults to 0 (int).
#    Useful for counters in nested structures.
category_item_counts = defaultdict(lambda: defaultdict(int))

category_item_counts['fruits']['apples'] += 5
category_item_counts['fruits']['bananas'] += 3
category_item_counts['vegetables']['carrots'] += 10
category_item_counts['fruits']['apples'] += 2 # Increment existing

print("\ndefaultdict(defaultdict(int)) example:")
# Convert to regular dict for cleaner printing if desired
print({k: dict(v) for k, v in category_item_counts.items()})
print(f"Apples count: {category_item_counts['fruits']['apples']}")
print(f"Broccoli count (new category/item): {category_item_counts['greens']['broccoli']}") # Accessing creates it with 0

# Expected Output:
# defaultdict(dict) example:
# {'user': {'name': 'Alice', 'email': 'alice@example.com'}, 'system': {'theme': 'dark'}}
# User name: Alice
#
# defaultdict(defaultdict(int)) example:
# {'fruits': {'apples': 7, 'bananas': 3}, 'vegetables': {'carrots': 10}, 'greens': {'broccoli': 0}}
# Apples count: 7
# Broccoli count (new category/item): 0