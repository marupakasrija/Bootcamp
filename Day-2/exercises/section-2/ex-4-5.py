from contextlib import suppress
import os

filename = "non_existent.txt"

with suppress(FileNotFoundError):
    with open(filename, 'r') as f:
        content = f.read()
        print(content)

print("Continuing after potentially missing file.")

# This will not raise an error, and the "Continuing..." message will be printed.