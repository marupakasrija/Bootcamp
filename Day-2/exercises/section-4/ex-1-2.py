def make_doubler():
  """Returns a function that doubles its input."""
  def doubler(x):
    return x * 2
  return doubler

# Example:
double_func = make_doubler()
result = double_func(7)
print(f"double_func(7): {result}") # Output: 14

result2 = make_doubler()(15)
print(f"make_doubler()(15): {result2}") # Output: 30