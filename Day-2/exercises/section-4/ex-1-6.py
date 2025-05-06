data_list = [(1, "b"), (2, "a"), (3, "c")]
sorted_list = sorted(data_list, key=lambda item: item[1])

print(f"Sorting {data_list} by the second element: {sorted_list}")
# Output: Sorting [(1, 'b'), (2, 'a'), (3, 'c')] by the second element: [(2, 'a'), (1, 'b'), (3, 'c')]