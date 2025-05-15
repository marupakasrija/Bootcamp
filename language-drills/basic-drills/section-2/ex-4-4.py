import time
from contextlib import contextmanager

@contextmanager
def timer():
    start_time = time.time()
    yield  # The code within the 'with' block will execute here
    end_time = time.time()
    elapsed_time = end_time - start_time
    print(f"Elapsed time: {elapsed_time:.4f} seconds")

with timer():
    time.sleep(1)
    print("Task completed.")