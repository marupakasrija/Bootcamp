# Using a generator
def even_numbers_generator(n):
    for i in range(n):
        if i % 2 == 0:
            yield i

even_gen = even_numbers_generator(5)
print("Generator output:")
for num in even_gen:
    print(num)

# Using a list comprehension
even_list = [num for num in range(5) if num % 2 == 0]
print("\nList comprehension output:")
for num in even_list:
    print(num)