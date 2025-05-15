def make_adder(n):
  """Returns a lambda function that adds 'n' to its argument."""
  return lambda x: x + n

# Example:
add_five = make_adder(5)
result = add_five(10)
print(f"add_five(10): {result}") # Output: 15

add_three = make_adder(3)
result2 = add_three(10)
print(f"add_three(10): {result2}") # Output: 13