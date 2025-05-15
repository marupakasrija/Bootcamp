len = 5

try:
    length = len("hello")
    print(length)
except TypeError as e:
    print(f"Error: {e}")
    # Output: Error: 'int' object is not callable