import itertools

original_iterator = iter(range(5)) # 0, 1, 2, 3, 4

iter1, iter2 = itertools.tee(original_iterator, 2) # Create two independent iterators

print("Iterating with iter1:")
for item in iter1:
  print(item, end=" ") # Output: 0 1 2 3 4
print("\n")

print("Iterating with iter2 (should be independent):")
for item in iter2:
  print(item, end=" ") # Output: 0 1 2 3 4
print("\n")

# Demonstrate partial consumption
data_source = (x*x for x in range(6)) # 0, 1, 4, 9, 16, 25
source1, source2 = itertools.tee(data_source)

print(f"First two from source1: {next(source1)}, {next(source1)}") # 0, 1
print("All from source2:")
for val in source2:
    print(val, end=" ") # 0 1 4 9 16 25
print("\nRemaining from source1:")
for val in source1:
    print(val, end=" ") # 4 9 16 25
print()

# Important note: Once tee has been used, the original_iterator should not be used anymore.
# Also, if one of the teed iterators is advanced far ahead of the others,
# tee may need to store all intervening items in memory.