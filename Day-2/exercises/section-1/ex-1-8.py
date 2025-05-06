my_tuple = (1, 2, 3)
try:
    my_tuple[0] = 10
except TypeError as e:
    print(f"Error: {e}")