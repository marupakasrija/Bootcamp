import itertools

def read_large_log_file(filename):
    """Simulates reading a large log file."""
    for i in range(100):
        yield f"Log entry number {i+1}"

first_ten_lines = itertools.islice(read_large_log_file("dummy.log"), 10)
for line in first_ten_lines:
    print(line)