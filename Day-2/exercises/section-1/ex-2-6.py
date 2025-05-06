import sys

list_comp = [x for x in range(1000000)]
generator_exp = (x for x in range(1000000))

list_size = sys.getsizeof(list_comp)
generator_size = sys.getsizeof(generator_exp)

print(f"Memory used by list comprehension: {list_size} bytes")
print(f"Memory used by generator expression: {generator_size} bytes")