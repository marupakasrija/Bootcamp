def to_uppercase(line: str) -> str:
    """
    Processor function: Converts the input line to uppercase after stripping whitespace.
    Expected signature: str -> str (will be wrapped by the engine in L4)
    """
    # print(f"DEBUG: Applying to_uppercase to '{line.strip()}'", file=sys.stderr)
    return line.strip().upper()

