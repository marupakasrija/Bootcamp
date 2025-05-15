def risky_operation(value):
    try:
        return 10 / value
    except ZeroDivisionError as e:
        print(f"Error type: {type(e)}, Error message: {e}")
        return None
    except Exception as e:
        print(f"Error type: {type(e)}, Error message: {e}")
        return None

if __name__ == "__main__":
    result1 = risky_operation(5)
    print(f"Result 1: {result1}")
    result2 = risky_operation(0)
    print(f"Result 2: {result2}")
    result3 = risky_operation("abc")
    print(f"Result 3: {result3}")