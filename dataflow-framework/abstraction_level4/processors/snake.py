def to_snakecase(line: str) -> str:
    """
    Processor function: Converts the input line to snake_case after stripping whitespace.
    Expected signature: str -> str (will be wrapped by the engine in L4)
    """
    # print(f"DEBUG: Applying to_snakecase to '{line.strip()}'", file=sys.stderr)
    return line.strip().lower().replace(" ", "_")


