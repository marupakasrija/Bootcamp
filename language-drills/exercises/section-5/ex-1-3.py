from collections import Counter

numbers = [1, 2, 2, 3, 3, 3, 4, 4, 4, 4, 5, 5, 5, 5, 5, 1, 2, 3]
number_counts = Counter(numbers)
most_common_two = number_counts.most_common(2)

print(f"Original list: {numbers}")
print(f"Two most common elements: {most_common_two}")

# Expected Output:
# Original list: [1, 2, 2, 3, 3, 3, 4, 4, 4, 4, 5, 5, 5, 5, 5, 1, 2, 3]
# Two most common elements: [(5, 5), (3, 4)] or [(5,5), (4,4)] if numbers list is slightly different,
# based on the example I made up just now, it is: [(5, 5), (4, 4)] then [(3,4)]
# Let's re-verify the list for [(5, 5), (3, 4)] as example:
numbers_updated = [1, 5, 2, 5, 3, 5, 4, 5, 1, 5, 2, 3, 3, 4, 3] # 5: five times, 3: four times
number_counts_updated = Counter(numbers_updated)
most_common_two_updated = number_counts_updated.most_common(2)
print(f"\nUpdated list: {numbers_updated}")
print(f"Two most common elements (updated): {most_common_two_updated}")

# Expected Output (for numbers_updated):
# Updated list: [1, 5, 2, 5, 3, 5, 4, 5, 1, 5, 2, 3, 3, 4, 3]
# Two most common elements (updated): [(5, 5), (3, 4)]