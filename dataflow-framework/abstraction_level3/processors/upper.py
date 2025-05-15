def to_uppercase(line: str) -> str:
    """
    Processor function: Converts the input line to uppercase after stripping whitespace.
    Expected signature: str -> str
    """
    # print(f"DEBUG: Applying to_uppercase to '{line.strip()}'") # Optional debug print
    return line.strip().upper()

