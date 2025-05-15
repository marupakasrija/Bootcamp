numbers = [1, 2, 3]
letters = ['a', 'b', 'c']

zipped = zip(numbers, letters)
print(list(zipped))

# Iterating through the zipped object
numbers2 = [10, 20, 30, 40]
letters2 = ['x', 'y', 'z']
zipped2 = zip(numbers2, letters2)
print("\nIterating through zipped:")
for num, letter in zipped2:
    print(f"Number: {num}, Letter: {letter}")

# Note: zip stops when the shortest iterable is exhausted
numbers3 = [1, 2, 3]
letters3 = ['p', 'q']
zipped3 = zip(numbers3, letters3)
print("\nZipping unequal length lists:")
print(list(zipped3))