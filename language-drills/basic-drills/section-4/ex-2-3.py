import time
import functools

def timer(func):
  @functools.wraps(func)
  def wrapper(*args, **kwargs):
    start_time = time.perf_counter()
    result = func(*args, **kwargs)
    end_time = time.perf_counter()
    elapsed_time = end_time - start_time
    print(f"Function '{func.__name__}' took {elapsed_time:.4f} seconds to execute.")
    return result
  return wrapper

@timer
def slow_function(duration):
  time.sleep(duration)
  return "Done sleeping"

result = slow_function(0.5)
print(result)
# Output (the time will vary slightly):
# Function 'slow_function' took 0.500X seconds to execute.
# Done sleeping