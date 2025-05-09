import sys
for line in sys.stdin:
    # Strip whitespace
    stripped_line = line.strip()
    # Convert to uppercase
    processed_line = stripped_line.upper()
    # Print to stdout
    print(processed_line)
# No functions, no classes, just sequential logic.