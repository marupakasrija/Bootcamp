data = [(1, 'b'), (3, 'a'), (2, 'c')]

sorted_by_second = sorted(data, key=lambda item: item[1])
print(f"Sorted by second item: {sorted_by_second}")

# Sorting a list of dictionaries by a specific key
people = [{'name': 'Alice', 'age': 30}, {'name': 'Bob', 'age': 25}, {'name': 'Charlie', 'age': 35}]
sorted_by_age = sorted(people, key=lambda person: person['age'])
print(f"Sorted by age: {sorted_by_age}")