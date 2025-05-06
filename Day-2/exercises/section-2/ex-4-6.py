import tempfile

with tempfile.TemporaryFile(mode='w+') as tmp_file:
    tmp_file.write("Hello temporary world!\n")
    tmp_file.seek(0)  # Go back to the beginning of the file
    content = tmp_file.read()
    print(f"Content of temporary file: {content.strip()}")

# The temporary file is automatically deleted when the 'with' block exits.