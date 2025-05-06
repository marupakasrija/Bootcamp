def process_file(filename):
    file = None
    try:
        file = open(filename, 'r')
        content = file.read()
        print(f"File content: {content}")
    except FileNotFoundError:
        print(f"Error: File '{filename}' not found.")
    finally:
        if file:
            file.close()
            print("Cleanup done: File closed.")
        else:
            print("Cleanup done: No file to close.")

process_file("existing_file.txt") # Create an empty file named 'existing_file.txt'
process_file("non_existent_file.txt")