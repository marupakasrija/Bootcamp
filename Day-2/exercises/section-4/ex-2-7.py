import functools
import time

def retry(max_tries, delay_seconds=1):
  def decorator(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
      attempts = 0
      while attempts < max_tries:
        try:
          print(f"Attempt {attempts + 1} for {func.__name__}...")
          return func(*args, **kwargs)
        except Exception as e:
          attempts += 1
          print(f"Exception caught in {func.__name__}: {e}. Retrying in {delay_seconds}s...")
          if attempts >= max_tries:
            print(f"Function {func.__name__} failed after {max_tries} attempts.")
            raise # Re-raise the last exception
          time.sleep(delay_seconds)
    return wrapper
  return decorator

# Example usage:
call_count = 0
@retry(max_tries=3, delay_seconds=0.1)
def might_fail_function():
  global call_count
  call_count += 1
  if call_count < 3:
    raise ValueError(f"Simulated error on attempt {call_count}")
  print("Function succeeded!")
  return "Success"

try:
  result = might_fail_function()
  print(f"Result: {result}")
except ValueError as e:
  print(f"Caught final error: {e}")

# Output:
# Attempt 1 for might_fail_function...
# Exception caught in might_fail_function: Simulated error on attempt 1. Retrying in 0.1s...
# Attempt 2 for might_fail_function...
# Exception caught in might_fail_function: Simulated error on attempt 2. Retrying in 0.1s...
# Attempt 3 for might_fail_function...
# Function succeeded!
# Result: Success

print("\n--- Another example that will fail completely ---")
another_call_count = 0
@retry(max_tries=2, delay_seconds=0.1)
def always_fails():
    global another_call_count
    another_call_count += 1
    raise ConnectionError(f"Network issue on attempt {another_call_count}")

try:
    always_fails()
except ConnectionError as e:
    print(f"Caught final error after retries: {e}")

# Output:
# --- Another example that will fail completely ---
# Attempt 1 for always_fails...
# Exception caught in always_fails: Network issue on attempt 1. Retrying in 0.1s...
# Attempt 2 for always_fails...
# Exception caught in always_fails: Network issue on attempt 2. Retrying in 0.1s...
# Function always_fails failed after 2 attempts.
# Caught final error after retries: Network issue on attempt 2