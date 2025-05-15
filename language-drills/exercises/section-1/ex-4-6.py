def make_multiplier(n):
    def multiplier(x):
        return x * n
    return multiplier

triple = make_multiplier(3)
result = triple(10)
print(result)  # Output: 30