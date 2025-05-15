filename = "example.txt"
# Create a dummy file
with open(filename, 'w') as f:
    f.write("This is some content.\n")
    f.write("Another line.")

try:
    with open(filename, 'r') as f:
        content = f.read()
        print(f"File content:\n{content}")
except FileNotFoundError:
    print(f"Error: File '{filename}' not found.")