file1_name = "file1.txt"
file2_name = "file2.txt"

# Create dummy files
with open(file1_name, 'w') as f1, open(file2_name, 'w') as f2:
    f1.write("Content of file 1.\n")
    f2.write("Content of file 2.\n")

try:
    with open(file1_name, 'r') as f1, open(file2_name, 'r') as f2:
        content1 = f1.read()
        content2 = f2.read()
        print(f"Content of {file1_name}:\n{content1}")
        print(f"\nContent of {file2_name}:\n{content2}")
except FileNotFoundError as e:
    print(f"Error: {e}")