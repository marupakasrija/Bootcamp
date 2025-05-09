def to_snakecase(line: str) -> str:
    """
    Processor function: Converts the input line to snake_case after stripping whitespace.
    Expected signature: str -> str
    """
    # print(f"DEBUG: Applying to_snakecase to '{line.strip()}'") 
    return line.strip().lower().replace(" ", "_")

