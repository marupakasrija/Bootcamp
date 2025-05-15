b = [1, 2, 3]
a = b
a.append(4)
print(f"a: {a}, b: {b}")  # Both a and b are modified

b = [1, 2, 3]
a = b[:]
a.append(4)
print(f"a: {a}, b: {b}")  # Only a is modified