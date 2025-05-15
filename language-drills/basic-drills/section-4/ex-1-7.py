def compose(f, g):
  """Returns a function that is the composition of f and g (f(g(x)))."""
  return lambda x: f(g(x))

# Example:
def add_one(x):
  return x + 1

def multiply_by_three(x):
  return x * 3

composed_func = compose(add_one, multiply_by_three)
result = composed_func(5) # add_one(multiply_by_three(5)) = add_one(15) = 16
print(f"compose(add_one, multiply_by_three)(5): {result}") # Output: 16