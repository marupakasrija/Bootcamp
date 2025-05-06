# Using sum with a generator expression (efficient)
sum_of_squares_efficient = sum(x*x for x in range(1000000))
print(f"Sum of squares (efficient): {sum_of_squares_efficient}")

# Using sum with a list comprehension (less efficient due to temporary list)
# sum_of_squares_inefficient = sum([x*x for x in range(1000000)])
# print(f"Sum of squares (inefficient): {sum_of_squares_inefficient}")