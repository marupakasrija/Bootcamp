my_list = ["apple", "banana", "cherry"]

# Without enumerate
print("Without enumerate:")
index = 0
for item in my_list:
    print(f"Index: {index}, Item: {item}")
    index += 1

# With enumerate
print("\nWith enumerate:")
for index, item in enumerate(my_list):
    print(f"Index: {index}, Item: {item}")

# Starting index from 1
print("\nWith enumerate (starting from 1):")
for index, item in enumerate(my_list, start=1):
    print(f"Index: {index}, Item: {item}")