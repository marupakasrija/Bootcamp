def apply(func, value):
  """Applies a function to a value."""
  return func(value)

# Example:
def square(x):
  return x * x

result = apply(square, 5)
print(f"apply(square, 5): {result}") # Output: 25

result_lambda = apply(lambda x: x * 2, 10)
print(f"apply(lambda x: x * 2, 10): {result_lambda}") # Output: 20