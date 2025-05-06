import warnings

def old_function(data):
    warnings.warn("The 'old_function' is deprecated and will be removed in future versions.", DeprecationWarning)
    return data * 2

if __name__ == "__main__":
    result = old_function(5)
    print(f"Result from old function: {result}")

    warnings.warn("This is a custom warning message.", UserWarning)