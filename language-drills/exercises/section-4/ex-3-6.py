from collections import defaultdict
import functools

# A common way to create a default dict that itself returns a default dict (for nesting)
# is using a lambda:
# tree = lambda: defaultdict(tree)
# my_tree = tree()
# my_tree['menu']['id'] = 'file'

# Using functools.partial to achieve a fixed-depth nested defaultdict:

# Level 1: A defaultdict that creates simple dicts for its missing keys
default_dict_level1_factory = functools.partial(defaultdict, dict)
d1 = default_dict_level1_factory()
d1['a']['b'] = 1
print(f"d1: {d1}") # Output: d1: defaultdict(<class 'dict'>, {'a': {'b': 1}})

# For truly nested structures (like the tree example),
# you typically need a callable that can be recursively defined.
# `partial` is more about fixing arguments to an existing function.

# Let's create a factory for a defaultdict that produces integers by default (like a counter)
int_default_dict_factory = functools.partial(defaultdict, int)
counter = int_default_dict_factory()
counter['apple'] += 1
counter['banana'] += 5
print(f"Counter: {counter}") # Output: Counter: defaultdict(<class 'int'>, {'apple': 1, 'banana': 5})


# If the goal is to create a function that, when called, generates a new nested dict structure:
def create_nested_dict_structure():
    """Returns a new nested defaultdict."""
    # This creates a defaultdict where missing keys default to being new defaultdicts,
    # which in turn default to int.
    level2_factory = functools.partial(defaultdict, int)
    level1_factory = functools.partial(defaultdict, level2_factory)
    return level1_factory()

nested = create_nested_dict_structure()
nested['category1']['itemA'] = 10
nested['category1']['itemB'] += 5 # Accessing will create itemB with 0, then add 5
nested['category2']['itemC'] = 100
print(f"Nested dict: {nested}")
# Output: Nested dict: defaultdict(<functools.partial object at ...>, {'category1': defaultdict(<class 'int'>, {'itemA': 10, 'itemB': 5}), 'category2': defaultdict(<class 'int'>, {'itemC': 100})})