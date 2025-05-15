squares_generator = (n*n for n in range(5))

print("First way (iterating):")
for square in squares_generator:
    print(square)

squares_generator = (n*n for n in range(5)) # Recreate the generator as it's exhausted
print("\nSecond way (using next()):")
print(next(squares_generator))
print(next(squares_generator))
print(next(squares_generator))
print(next(squares_generator))
print(next(squares_generator))
try:
    print(next(squares_generator)) # Raises StopIteration
except StopIteration:
    print("Generator exhausted")