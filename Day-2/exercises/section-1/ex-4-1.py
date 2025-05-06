x = 10  # Global variable

def my_function():
    x = 20  # Local variable
    print(f"Local x: {x}")

my_function()
print(f"Global x: {x}")