import functools

def simple_logger(func):
  @functools.wraps(func) # Good practice to preserve metadata
  def wrapper(*args, **kwargs):
    print(f"Function '{func.__name__}' started")
    result = func(*args, **kwargs)
    print(f"Function '{func.__name__}' ended")
    return result
  return wrapper

@simple_logger
def greet(name):
  print(f"Hello, {name}!")

@simple_logger
def add(a, b):
  return a + b

greet("Alice")
# Output:
# Function 'greet' started
# Hello, Alice!
# Function 'greet' ended

sum_result = add(10, 5)
print(f"Sum: {sum_result}")
# Output:
# Function 'add' started
# Function 'add' ended
# Sum: 15