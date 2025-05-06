numbers1 = [1, 2, -3, 4, 5]
numbers2 = [10, 20, 30, 40, 50]
numbers3 = [-1, -2, -3]

has_negative = any(num < 0 for num in numbers1)
all_positive1 = all(num > 0 for num in numbers1)
all_positive2 = all(num > 0 for num in numbers2)
all_negative = all(num < 0 for num in numbers3)

print(f"List 1 has any negative numbers: {has_negative}")
print(f"All numbers in List 1 are positive: {all_positive1}")
print(f"All numbers in List 2 are positive: {all_positive2}")
print(f"All numbers in List 3 are negative: {all_negative}")