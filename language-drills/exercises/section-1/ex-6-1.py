my_list = [10, 20, 30]
my_iterator = iter(my_list)

print(next(my_iterator))
print(next(my_iterator))
print(next(my_iterator))
try:
    print(next(my_iterator))
except StopIteration:
    print("End of iteration.")