from collections import defaultdict
import functools

# Factory for a list
list_factory = functools.partial(list)
d_list = defaultdict(list_factory)
d_list['key1'].append(1)
print(f"Defaultdict with list factory from partial: {d_list}")
# Output: Defaultdict with list factory from partial: defaultdict(<function list>, {'key1': [1]})

# Factory for a dict (less common as defaultdict(dict) is simpler)
dict_factory_via_partial = functools.partial(dict)
d_dict_p = defaultdict(dict_factory_via_partial)
d_dict_p['key1']['subkey'] = 'value'
print(f"Defaultdict with dict factory from partial: {d_dict_p}")
# Output: Defaultdict with dict factory from partial: defaultdict(<function dict>, {'key1': {'subkey': 'value'}})