import functools

def custom_logger(log_message_before, log_message_after=None):
  if log_message_after is None:
    log_message_after = log_message_before # Default to same message if only one provided
  def decorator(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
      print(f"{log_message_before} - Starting '{func.__name__}'")
      result = func(*args, **kwargs)
      print(f"{log_message_after} - Finished '{func.__name__}'")
      return result
    return wrapper
  return decorator

@custom_logger("PROCESS: Data Ingestion", "PROCESS: Ingestion Complete")
def ingest_data(source):
  print(f"Ingesting data from {source}...")
  return f"Data from {source} processed."

@custom_logger("TASK") # Uses the same message before and after
def simple_task():
    print("Executing simple task...")
    return "Task done."


ingest_result = ingest_data("API Endpoint")
print(ingest_result)
# Output:
# PROCESS: Data Ingestion - Starting 'ingest_data'
# Ingesting data from API Endpoint...
# PROCESS: Ingestion Complete - Finished 'ingest_data'
# Data from API Endpoint processed.

task_res = simple_task()
print(task_res)
# Output:
# TASK - Starting 'simple_task'
# Executing simple task...
# TASK - Finished 'simple_task'
# Task done.