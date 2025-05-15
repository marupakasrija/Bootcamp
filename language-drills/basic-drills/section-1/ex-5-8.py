def outer_function(filename):
    try:
        with open(filename, 'r') as f:
            try:
                content = f.readline().strip()
                number = int(content)
                result = 100 / number
                print(f"Result: {result}")
            except ValueError:
                print("Inner Error: Invalid number format in file.")
            except ZeroDivisionError:
                print("Inner Error: Cannot divide by zero in file.")
    except FileNotFoundError:
        print(f"Outer Error: File '{filename}' not found.")

# Create a file named 'data1.txt' with content '10'
with open("data1.txt", "w") as f:
    f.write("10")

# Create a file named 'data2.txt' with content 'abc'
with open("data2.txt", "w") as f:
    f.write("abc")

# Create a file named 'data3.txt' with content '0'
with open("data3.txt", "w") as f:
    f.write("0")

outer_function("data1.txt")
outer_function("data2.txt")
outer_function("data3.txt")
outer_function("missing_file.txt")