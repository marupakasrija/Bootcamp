my_list = [1, 2, 3, 4, 5]
a, b, *rest = my_list
print(f"a: {a}")
print(f"b: {b}")
print(f"rest: {rest}")

first, *middle, last = [10, 20, 30, 40]
print(f"\nFirst: {first}")
print(f"Middle: {middle}")
print(f"Last: {last}")