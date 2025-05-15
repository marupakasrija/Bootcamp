def outer_function(message):
    def inner_function():
        print(f"Message from outer function: {message}")
    inner_function()

outer_function("Hello from outer!")