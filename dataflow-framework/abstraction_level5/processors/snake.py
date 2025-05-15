# This is abstraction-level-5/processors/snake.py
# Contains a processor adapted for Level 5 DAG, yielding tagged lines.

import sys # Needed for sys.stderr
from typing import Iterator, Optional, Tuple
# Import base class and types using relative imports from the parent package
from ..types import TaggedStreamProcessor, ProcessorConfig, TaggedLine

class SnakecaseProcessor(TaggedStreamProcessor):
    """
    Stream processor that converts lines to snake_case and yields with a fixed tag.
    Inherits from TaggedStreamProcessor.
    """
    def __init__(self, name: str, config: Optional[ProcessorConfig] = None):
        super().__init__(name, config)
        # Configurable output tag, defaults to 'processed'
        self.output_tag = self.config.get("output_tag", "processed")
        # print(f"DEBUG: Initialized SnakecaseProcessor '{self.name}' with output_tag='{self.output_tag}'", file=sys.stderr) # Optional debug

    def process(self, lines: Iterator[str]) -> Iterator[TaggedLine]:
        """Processes lines, converts to snake_case, and yields (output_tag, line)."""
        # print(f"DEBUG: SnakecaseProcessor '{self.name}' processing stream...", file=sys.stderr) # Optional debug
        for line in lines:
            processed_line = line.strip().lower().replace(" ", "_")
            # print(f"DEBUG: SnakecaseProcessor '{self.name}' yielding ('{self.output_tag}', '{processed_line}')", file=sys.stderr) # Optional debug
            yield (self.output_tag, processed_line)
        # print(f"DEBUG: SnakecaseProcessor '{self.name}' finished stream.", file=sys.stderr) # Optional debug

# The old str->str function is no longer used directly by the engine.
# def to_snakecase(line: str) -> str:
#     return line.strip().lower().replace(" ", "_")

