import functools
import datetime

def logging_decorator_with_wraps(func):
  @functools.wraps(func) # Preserves metadata like __name__, __doc__
  def wrapper(*args, **kwargs):
    timestamp_before = datetime.datetime.now().isoformat()
    print(f"LOG [{timestamp_before}]: Calling function '{func.__name__}' with args: {args}, kwargs: {kwargs}")
    result = func(*args, **kwargs)
    timestamp_after = datetime.datetime.now().isoformat()
    print(f"LOG [{timestamp_after}]: Function '{func.__name__}' finished. Returned: {result}")
    return result
  return wrapper

@logging_decorator_with_wraps
def process_data(data, config=None):
  """Processes the given data according to the config."""
  print(f"  Processing: {data}")
  processed_info = f"Processed_{data}_with_config_{config}"
  return processed_info

print(f"Function name: {process_data.__name__}")
print(f"Function docstring: {process_data.__doc__}")
output = process_data("SampleData", config={"mode": "fast"})
print(f"Final output: {output}")

# Output:
# Function name: process_data
# Function docstring: Processes the given data according to the config.
# LOG [YYYY-MM-DDTHH:MM:SS.micros]: Calling function 'process_data' with args: ('SampleData',), kwargs: {'config': {'mode': 'fast'}}
#   Processing: SampleData
# LOG [YYYY-MM-DDTHH:MM:SS.micros]: Function 'process_data' finished. Returned: Processed_SampleData_with_config_{'mode': 'fast'}
# Final output: Processed_SampleData_with_config_{'mode': 'fast'}