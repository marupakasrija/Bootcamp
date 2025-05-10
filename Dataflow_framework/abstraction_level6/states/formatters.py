# This is abstraction-level-6/states/formatters.py
# Contains formatting state processors.

import sys # Needed for sys.stderr
from typing import Iterator, Optional, Tuple
# Import base class and types using relative imports from the parent package (states)
from ..types import StateProcessor, ProcessorConfig, TaggedLine

class UppercaseFormatter(StateProcessor):
    """
    A state processor that converts lines to uppercase and yields with a fixed next tag.
    """
    def __init__(self, tag: str, config: Optional[ProcessorConfig] = None):
        super().__init__(tag, config)
        self.next_tag = self.config.get("next_tag", "processed")
        # print(f"DEBUG: Initialized UppercaseFormatter for state '{self.tag}' with next_tag='{self.next_tag}'", file=sys.stderr) # Optional debug

    def process(self, lines: Iterator[TaggedLine]) -> Iterator[TaggedLine]:
        """Processes lines, converts to uppercase, and yields (next_tag, line)."""
        # print(f"DEBUG: UppercaseFormatter for state '{self.tag}' processing stream...", file=sys.stderr) # Optional debug
        for incoming_tag, line in lines:
            processed_line = line.strip().upper()
            # print(f"DEBUG: UppercaseFormatter '{self.tag}' yielding ('{self.next_tag}', '{processed_line}')", file=sys.stderr) # Optional debug
            yield (self.next_tag, processed_line)
        # print(f"DEBUG: UppercaseFormatter for state '{self.tag}' finished stream.", file=sys.stderr) # Optional debug


class SnakecaseFormatter(StateProcessor):
    """
    A state processor that converts lines to snake_case and yields with a fixed next tag.
    """
    def __init__(self, tag: str, config: Optional[ProcessorConfig] = None):
        super().__init__(tag, config)
        self.next_tag = self.config.get("next_tag", "processed")
        # print(f"DEBUG: Initialized SnakecaseFormatter for state '{self.tag}' with next_tag='{self.next_tag}'", file=sys.stderr) # Optional debug


    def process(self, lines: Iterator[TaggedLine]) -> Iterator[TaggedLine]:
        """Processes lines, converts to snake_case, and yields (next_tag, line)."""
        # print(f"DEBUG: SnakecaseFormatter for state '{self.tag}' processing stream...", file=sys.stderr) # Optional debug
        for incoming_tag, line in lines:
            processed_line = line.strip().lower().replace(" ", "_")
            # print(f"DEBUG: SnakecaseFormatter '{self.tag}' yielding ('{self.next_tag}', '{processed_line}')", file=sys.stderr) # Optional debug
            yield (self.next_tag, processed_line)
        # print(f"DEBUG: SnakecaseFormatter for state '{self.tag}' finished stream.", file=sys.stderr) # Optional debug

