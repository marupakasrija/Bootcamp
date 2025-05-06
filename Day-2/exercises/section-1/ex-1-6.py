a = {1, 2, 3}
b = {3, 4}

intersection = a.intersection(b)
union = a.union(b)
difference_ab = a.difference(b)
difference_ba = b.difference(a)

print(f"Intersection (a & b): {intersection}")
print(f"Union (a | b): {union}")
print(f"Difference (a - b): {difference_ab}")
print(f"Difference (b - a): {difference_ba}")