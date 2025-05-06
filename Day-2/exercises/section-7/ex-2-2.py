import sys

# Generator expression
generator = (x*x for x in range(1000000))
print(f"Size of generator: {sys.getsizeof(generator)} bytes")

# List comprehension
list_comp = [x*x for x in range(1000000)]
print(f"Size of list comprehension: {sys.getsizeof(list_comp)} bytes")