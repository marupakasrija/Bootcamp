def add(x, y):
    """Adds two numbers."""
    return x + y

def subtract(x, y):
    """Subtracts the second number from the first."""
    return x - y

def multiply(x, y):
    """Multiplies two numbers."""
    return x * y

def divide(x, y):
    """Divides the first number by the second."""
    if y == 0:
        raise ValueError("Cannot divide by zero")
    return x / y

def perform_operation(operation, num1, num2):
    """Performs the specified arithmetic operation."""
    if operation == "add":
        return add(num1, num2)
    elif operation == "subtract":
        return subtract(num1, num2)
    elif operation == "multiply":
        return multiply(num1, num2)
    elif operation == "divide":
        return divide(num1, num2)
    else:
        raise ValueError(f"Unknown operation: {operation}")

if __name__ == "__main__":
    result_add = perform_operation("add", 5, 3)
    print(f"5 + 3 = {result_add}")
    result_divide = perform_operation("divide", 10, 2)
    print(f"10 / 2 = {result_divide}")

# Original long function:
# def calculate(op, a, b):
#     if op == "+":
#         return a + b
#     elif op == "-":
#         return a - b
#     elif op == "*":
#         return a * b
#     elif op == "/":
#         if b == 0:
#             raise ValueError("...")
#         return a / b
#     else:
#         raise ValueError("...")