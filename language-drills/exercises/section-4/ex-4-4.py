import itertools

list1 = [1, 2]
list2 = [3, 4]
list3 = [5]

combined_iterator = itertools.chain(list1, list2, list3)
flattened_list = list(combined_iterator)

print(f"Flattened list using chain: {flattened_list}")
# Output: Flattened list using chain: [1, 2, 3, 4, 5]

# Can also use chain.from_iterable if you have a list of lists
list_of_lists = [[10, 20], [30, 40], [50]]
combined_from_iterable = itertools.chain.from_iterable(list_of_lists)
flattened_from_iterable = list(combined_from_iterable)
print(f"Flattened list using chain.from_iterable: {flattened_from_iterable}")
# Output: Flattened list using chain.from_iterable: [10, 20, 30, 40, 50]