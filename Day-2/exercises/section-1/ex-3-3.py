def add_all(*args):
    total = 0
    for num in args:
        total += num
    return total

print(add_all(1, 2, 3))       # Output: 6
print(add_all(10, 20, 30, 40)) # Output: 100
print(add_all())              # Output: 0