from typing import Iterator
from .types import ProcessorFn

def to_uppercase(line: str) -> str:
    """Processor: Converts line to uppercase."""
    return line.strip().upper()

def to_snakecase(line: str) -> str:
    """Processor: Converts line to snakecase."""
    return line.strip().lower().replace(" ", "_")

def apply_pipeline(lines: Iterator[str], pipeline: list[ProcessorFn]) -> Iterator[str]:
    """Applies a list of processors sequentially to each line."""
    for line in lines:
        processed_line = line
        for processor in pipeline:
            processed_line = processor(processed_line)
        yield processed_line