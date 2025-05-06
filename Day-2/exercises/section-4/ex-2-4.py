import functools
import time
def memoize(func):
  cache = {}
  @functools.wraps(func)
  def wrapper(*args, **kwargs):
    # Create a key from arguments (handling unhashable types like lists if necessary)
    key_args = args
    key_kwargs = tuple(sorted(kwargs.items()))
    key = (key_args, key_kwargs)

    if key not in cache:
      print(f"Calculating result for {func.__name__}{args}{kwargs}...")
      cache[key] = func(*args, **kwargs)
    else:
      print(f"Returning cached result for {func.__name__}{args}{kwargs}...")
    return cache[key]
  return wrapper

@memoize
def fibonacci(n):
  if n < 2:
    return n
  return fibonacci(n-1) + fibonacci(n-2)

print(f"fibonacci(5): {fibonacci(5)}")
# Output (shows calculation steps for the first call):
# Calculating result for fibonacci(5){}...
# Calculating result for fibonacci(4){}...
# Calculating result for fibonacci(3){}...
# Calculating result for fibonacci(2){}...
# Calculating result for fibonacci(1){}...
# Calculating result for fibonacci(0){}...
# Returning cached result for fibonacci(1){}...
# Returning cached result for fibonacci(2){}...
# Returning cached result for fibonacci(3){}...
# fibonacci(5): 5

print(f"fibonacci(5): {fibonacci(5)}") # Second call
# Output:
# Returning cached result for fibonacci(5){}...
# fibonacci(5): 5

@memoize
def complex_computation(a, b, option="default"):
    print(f"Performing complex computation with {a}, {b}, option='{option}'")
    time.sleep(0.1) # Simulate work
    return a * b + (len(option) if option else 0)

print(complex_computation(2, 3))
print(complex_computation(2, 3))
print(complex_computation(2, 3, option="special"))
print(complex_computation(2, 3, option="special"))
# Output:
# Calculating result for complex_computation(2, 3){}...
# Performing complex computation with 2, 3, option='default'
# 13
# Returning cached result for complex_computation(2, 3){}...
# 13
# Calculating result for complex_computation(2, 3){('option', 'special')}...
# Performing complex computation with 2, 3, option='special'
# 13
# Returning cached result for complex_computation(2, 3){('option', 'special')}...
# 13