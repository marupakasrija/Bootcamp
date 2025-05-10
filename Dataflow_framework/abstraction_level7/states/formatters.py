# This is abstraction-level-7/states/formatters.py
# Contains formatting state processors. Adapted for TracedLine.

import sys # Needed for sys.stderr
from typing import Iterator, Optional, Tuple
# Import base class and types using relative imports from the parent package (states)
from ..types import StateProcessor, ProcessorConfig, TracedLine

class UppercaseFormatter(StateProcessor):
    """
    A state processor that converts lines to uppercase and yields with a fixed next tag.
    Handles TracedLine.
    """
    def __init__(self, tag: str, config: Optional[ProcessorConfig] = None):
        super().__init__(tag, config)
        self.next_tag = self.config.get("next_tag", "processed")
        # print(f"DEBUG: Initialized UppercaseFormatter for state '{self.tag}' with next_tag='{self.next_tag}'", file=sys.stderr) # Optional debug

    def process(self, lines: Iterator[TracedLine]) -> Iterator[TracedLine]:
        """
        Processes lines received (as TracedLine), converts to uppercase,
        and yields (id, next_tag, processed_line, updated_history).
        """
        # print(f"DEBUG: UppercaseFormatter for state '{self.tag}' processing stream...", file=sys.stderr) # Optional debug
        for line_id, incoming_tag, line_content, history in lines:
            processed_line = line_content.strip().upper()
            updated_history = history + [self.tag] # Add current state to history
            # print(f"DEBUG: UppercaseFormatter '{self.tag}' yielding ('{line_id}', '{self.next_tag}', '{processed_line}', {updated_history})", file=sys.stderr) # Optional debug
            yield (line_id, self.next_tag, processed_line, updated_history)
        # print(f"DEBUG: UppercaseFormatter for state '{self.tag}' finished stream.", file=sys.stderr) # Optional debug


class SnakecaseFormatter(StateProcessor):
    """
    A state processor that converts lines to snake_case and yields with a fixed next tag.
    Handles TracedLine.
    """
    def __init__(self, tag: str, config: Optional[ProcessorConfig] = None):
        super().__init__(tag, config)
        self.next_tag = self.config.get("next_tag", "processed")
        # print(f"DEBUG: Initialized SnakecaseFormatter for state '{self.tag}' with next_tag='{self.next_tag}'", file=sys.stderr) # Optional debug


    def process(self, lines: Iterator[TracedLine]) -> Iterator[TracedLine]:
        """
        Processes lines received (as TracedLine), converts to snake_case,
        and yields (id, next_tag, processed_line, updated_history).
        """
        # print(f"DEBUG: SnakecaseFormatter for state '{self.tag}' processing stream...", file=sys.stderr) # Optional debug
        for line_id, incoming_tag, line_content, history in lines:
            processed_line = line_content.strip().lower().replace(" ", "_")
            updated_history = history + [self.tag] # Add current state to history
            # print(f"DEBUG: SnakecaseFormatter '{self.tag}' yielding ('{self.next_tag}', '{processed_line}', {updated_history})", file=sys.stderr) # Optional debug
            yield (line_id, self.next_tag, processed_line, updated_history)
        # print(f"DEBUG: SnakecaseFormatter for state '{self.tag}' finished stream.", file=sys.stderr) # Optional debug

