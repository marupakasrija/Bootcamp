def slow_function():
    result = 0
    for i in range(1000000):
        result += i
    return result

def fast_function():
    return sum(range(1000000))

if __name__ == "__main__":
    slow_function()
    fast_function()