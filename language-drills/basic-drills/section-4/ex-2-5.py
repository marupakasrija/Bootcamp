import functools

def debug_info(func):
  @functools.wraps(func)
  def wrapper(*args, **kwargs):
    args_repr = [repr(a) for a in args]
    kwargs_repr = [f"{k}={repr(v)}" for k, v in kwargs.items()]
    signature = ", ".join(args_repr + kwargs_repr)
    print(f"Calling: {func.__name__}({signature})")
    result = func(*args, **kwargs)
    print(f"{func.__name__} returned: {repr(result)}")
    return result
  return wrapper

@debug_info
def multiply(a, b, c=1):
  return a * b * c

product = multiply(2, 3)
# Output:
# Calling: multiply(2, 3)
# multiply returned: 6

product_with_kwarg = multiply(2, 3, c=5)
# Output:
# Calling: multiply(2, 3, c=5)
# multiply returned: 30