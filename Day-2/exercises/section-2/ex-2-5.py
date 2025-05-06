numbers = [1, 2, 3, 4, 5]

doubled = map(lambda x: x * 2, numbers)
print(f"Doubled numbers (map): {list(doubled)}")

evens_removed = filter(lambda x: x % 2 != 0, numbers)
print(f"Even numbers removed (filter): {list(evens_removed)}")