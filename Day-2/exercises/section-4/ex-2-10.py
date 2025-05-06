import functools
import time

# (Re-defining decorators from above for self-contained example)
def simple_logger(func):
  @functools.wraps(func)
  def wrapper(*args, **kwargs):
    print(f"SIMPLE_LOGGER: Function '{func.__name__}' started")
    result = func(*args, **kwargs)
    print(f"SIMPLE_LOGGER: Function '{func.__name__}' ended")
    return result
  return wrapper

def timer(func):
  @functools.wraps(func)
  def wrapper(*args, **kwargs):
    start_time = time.perf_counter()
    result = func(*args, **kwargs)
    end_time = time.perf_counter()
    elapsed_time = end_time - start_time
    print(f"TIMER: Function '{func.__name__}' took {elapsed_time:.6f} seconds.")
    return result
  return wrapper

def debug_info(func):
  @functools.wraps(func)
  def wrapper(*args, **kwargs):
    args_repr = [repr(a) for a in args]
    kwargs_repr = [f"{k}={repr(v)}" for k, v in kwargs.items()]
    signature = ", ".join(args_repr + kwargs_repr)
    print(f"DEBUG_INFO: Calling: {func.__name__}({signature})")
    result = func(*args, **kwargs)
    print(f"DEBUG_INFO: {func.__name__} returned: {repr(result)}")
    return result
  return wrapper

print("--- Order 1: simple_logger -> timer -> debug_info ---")
@simple_logger
@timer
@debug_info
def my_function_order1(x, y):
  print("Executing my_function_order1 core logic")
  time.sleep(0.01)
  return x + y

my_function_order1(10, 20)
# Decorators are applied from bottom up (closest to function first).
# So, debug_info wraps the original function.
# timer wraps the debug_info wrapper.
# simple_logger wraps the timer wrapper.
# Execution order is outer-to-inner for the "before" part, and inner-to-outer for the "after" part.

# Expected output order for "before":
# SIMPLE_LOGGER: Function 'my_function_order1' started
# TIMER: (start time captured)
# DEBUG_INFO: Calling: my_function_order1(10, 20)
# Executing my_function_order1 core logic
# DEBUG_INFO: my_function_order1 returned: 30
# TIMER: Function 'my_function_order1' took 0.01XXXX seconds.
# SIMPLE_LOGGER: Function 'my_function_order1' ended

print("\n--- Order 2: debug_info -> timer -> simple_logger ---")
@debug_info
@timer
@simple_logger
def my_function_order2(x, y):
  print("Executing my_function_order2 core logic")
  time.sleep(0.01)
  return x + y

my_function_order2(5, 3)
# Expected output order for "before":
# DEBUG_INFO: Calling: my_function_order2(5, 3)
# TIMER: (start time captured)
# SIMPLE_LOGGER: Function 'my_function_order2' started
# Executing my_function_order2 core logic
# SIMPLE_LOGGER: Function 'my_function_order2' ended
# TIMER: Function 'my_function_order2' took 0.01XXXX seconds.
# DEBUG_INFO: my_function_order2 returned: 8

# Observation:
# The order of decorators matters. The outermost decorator executes its "before" code first,
# and its "after" code last. The innermost decorator's "before" code runs just before the
# actual function, and its "after" code runs just after.
# For example, in Order 1, simple_logger starts, then timer starts (captures time),
# then debug_info logs call, function runs, debug_info logs return, timer logs duration,
# simple_logger ends.
# The `timer` decorator will time whatever it directly wraps.
# - In Order 1, `timer` wraps `debug_info(my_function_order1)`. So it times the execution of `debug_info`'s wrapper and the original function.
# - In Order 2, `timer` wraps `simple_logger(my_function_order2)`. So it times the execution of `simple_logger`'s wrapper and the original function.
# The print statements from the debug_info (e.g., "Calling...") or simple_logger will be *inside* or *outside* the timer's duration measurement based on their position relative to the timer.