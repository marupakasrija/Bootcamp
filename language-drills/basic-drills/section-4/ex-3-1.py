import functools

# Create a new function that converts a binary string to an integer
binary_to_int = functools.partial(int, base=2)

result1 = binary_to_int("101")
print(f"binary_to_int('101'): {result1}") # Output: 5

result2 = binary_to_int("1110")
print(f"binary_to_int('1110'): {result2}") # Output: 14

# For comparison:
# print(int("101", base=2))