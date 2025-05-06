nested_list = [[1, 2], [3, 4]]
flattened_list = [item for sublist in nested_list for item in sublist]
print(flattened_list)