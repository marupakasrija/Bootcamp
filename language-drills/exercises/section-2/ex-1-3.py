filename = "my_file.txt"

# EAFP
try:
    with open(filename, 'r') as f:
        content = f.read()
        print(f"File content: {content}")
except FileNotFoundError:
    print(f"Error: File '{filename}' not found.")

# LBYL (less common for file operations due to potential race conditions)
import os
if os.path.exists(filename):
    try:
        with open(filename, 'r') as f:
            content = f.read()
            print(f"File content (LBYL): {content}")
    except Exception as e:
        print(f"Error reading file (LBYL): {e}")
else:
    print(f"File '{filename}' not found (LBYL).")