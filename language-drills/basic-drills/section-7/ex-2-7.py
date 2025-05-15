def copy_file_streaming(source_filename, destination_filename):
    """Copies a file line by line."""
    try:
        with open(source_filename, 'r') as source, open(destination_filename, 'w') as destination:
            for line in source:
                destination.write(line)
        print(f"File '{source_filename}' copied to '{destination_filename}' successfully.")
    except FileNotFoundError:
        print("Source file not found.")
    except Exception as e:
        print(f"An error occurred during file copy: {e}")

if __name__ == "__main__":
    # Create a dummy source file
    with open("source.txt", "w") as f:
        f.write("This is the first line.\n")
        f.write("This is the second line.\n")
        f.write("This is the third line.\n")

    copy_file_streaming("source.txt", "destination.txt")