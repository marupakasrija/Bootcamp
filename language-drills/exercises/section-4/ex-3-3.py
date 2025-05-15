import functools

def my_simple_decorator(func):
  @functools.wraps(func) # This is the key part
  def wrapper(*args, **kwargs):
    """Wrapper's own docstring."""
    print(f"Decorator: Calling {func.__name__}")
    result = func(*args, **kwargs)
    print(f"Decorator: Finished {func.__name__}")
    return result
  return wrapper

@my_simple_decorator
def decorated_function(name):
  """This is the original docstring for decorated_function."""
  print(f"Hello, {name} from decorated_function!")
  return f"Greetings, {name}"

print(f"Function name: {decorated_function.__name__}")
print(f"Function docstring: {decorated_function.__doc__}")
decorated_function("World")

# Without @functools.wraps(func):
# Function name would be 'wrapper'
# Function docstring would be "Wrapper's own docstring."

# With @functools.wraps(func):
# Function name: decorated_function
# Function docstring: This is the original docstring for decorated_function.
# Decorator: Calling decorated_function
# Hello, World from decorated_function!
# Decorator: Finished decorated_function