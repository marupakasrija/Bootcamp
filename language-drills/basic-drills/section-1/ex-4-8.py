def scope_error_func():
    print(my_var)
    my_var = 10

try:
    scope_error_func()
except UnboundLocalError as e:
    print(f"Error: {e}")
    # Output: Error: local variable 'my_var' referenced before assignment