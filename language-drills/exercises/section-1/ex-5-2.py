def divide_else(a, b):
    try:
        result = a / b
        return result
    except ZeroDivisionError:
        print("Cannot divide by zero.")
        return None
    else:
        print("Division successful.")
        return result

print(divide_else(10, 2))
print(divide_else(5, 0))