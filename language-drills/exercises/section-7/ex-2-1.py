def read_large_file(filename):
    """Reads a large file line by line using a generator."""
    with open(filename, 'r') as file:
        for line in file:
            yield line.strip()

if __name__ == "__main__":
    # Create a dummy large file for demonstration
    with open("large_file.txt", "w") as f:
        for i in range(1000):
            f.write(f"Line {i}\n")

    for line in read_large_file("large_file.txt"):
        # Process each line without loading the entire file into memory
        if "Line 5" in line:
            print(f"Found: {line}")
            break