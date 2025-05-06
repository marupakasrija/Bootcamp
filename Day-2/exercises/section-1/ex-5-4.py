def calculate(a, b):
    try:
        num1 = int(a)
        num2 = int(b)
        result = num1 / num2
        return result
    except ValueError:
        print("Error: Invalid input. Please enter numbers.")
        return None
    except ZeroDivisionError:
        print("Error: Cannot divide by zero.")
        return None

print(calculate("10", "2"))
print(calculate("hello", "2"))
print(calculate("10", "0"))