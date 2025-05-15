def add_numbers(a: int, b: int) -> int:
    """Adds two integers and returns the sum."""
    return a + b

result = add_numbers(5, 3)
print(f"Sum: {result}")

# Type hints are for static analysis and don't cause runtime errors in standard Python
result_str = add_numbers("hello", "world")
print(f"Concatenated: {result_str}")