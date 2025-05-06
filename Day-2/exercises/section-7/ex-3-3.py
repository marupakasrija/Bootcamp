import traceback

def outer_function(a, b):
    return inner_function(a * 2, b / 0)

def inner_function(x, y):
    return x + y

if __name__ == "__main__":
    try:
        result = outer_function(5, 10)
        print(f"Result: {result}")
    except Exception:
        error_trace = traceback.format_exc()
        print("An error occurred:")
        print(error_trace)