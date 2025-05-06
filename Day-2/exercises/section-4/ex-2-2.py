import functools

def prefix_printer(prefix):
  def decorator(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
      print(f"{prefix}: Calling function '{func.__name__}'")
      result = func(*args, **kwargs)
      return result
    return wrapper
  return decorator

@prefix_printer("LOG")
def say_hello(name):
  print(f"Hello, {name}")

@prefix_printer("DEBUG")
def calculate_sum(x, y):
  return x + y

say_hello("Bob")
# Output:
# LOG: Calling function 'say_hello'
# Hello, Bob

result = calculate_sum(3, 7)
print(f"Calculation result: {result}")
# Output:
# DEBUG: Calling function 'calculate_sum'
# Calculation result: 10