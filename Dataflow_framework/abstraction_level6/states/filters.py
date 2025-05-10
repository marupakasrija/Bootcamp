# This is abstraction-level-6/states/filters.py
# Contains filtering state processors.

import sys # Needed for sys.stderr
from typing import Iterator, Optional, Tuple, Any, Dict
# Import base class and types using relative imports from the parent package (states)
from ..types import StateProcessor, ProcessorConfig, TaggedLine

class ErrorOnlyFilter(StateProcessor):
    """
    A state processor that only yields lines containing "ERROR", with a fixed next tag.
    Lines not containing "ERROR" are dropped (not yielded).
    """
    def __init__(self, tag: str, config: Optional[ProcessorConfig] = None):
        super().__init__(tag, config)
        self.next_tag = self.config.get("next_tag", "error_processed")
        # print(f"DEBUG: Initialized ErrorOnlyFilter for state '{self.tag}' with next_tag='{self.next_tag}'", file=sys.stderr) # Optional debug


    def process(self, lines: Iterator[TaggedLine]) -> Iterator[TaggedLine]:
        """Processes lines, yields only error lines with next_tag."""
        # print(f"DEBUG: ErrorOnlyFilter for state '{self.tag}' processing stream...", file=sys.stderr) # Optional debug
        for incoming_tag, line in lines:
            if "ERROR" in line:
                # print(f"DEBUG: ErrorOnlyFilter '{self.tag}' found ERROR, yielding ('{self.next_tag}', '{line}')", file=sys.stderr) # Optional debug
                yield (self.next_tag, line)
            # else: line is dropped (not yielded)
        # print(f"DEBUG: ErrorOnlyFilter for state '{self.tag}' finished stream.", file=sys.stderr) # Optional debug


class WarnOnlyFilter(StateProcessor):
    """
    A state processor that only yields lines containing "WARN", with a fixed next tag.
    Lines not containing "WARN" are dropped (not yielded).
    """
    def __init__(self, tag: str, config: Optional[ProcessorConfig] = None):
        super().__init__(tag, config)
        self.next_tag = self.config.get("next_tag", "warn_processed")
        # print(f"DEBUG: Initialized WarnOnlyFilter for state '{self.tag}' with next_tag='{self.next_tag}'", file=sys.stderr) # Optional debug


    def process(self, lines: Iterator[TaggedLine]) -> Iterator[TaggedLine]:
        """Processes lines, yields only warn lines with next_tag."""
        # print(f"DEBUG: WarnOnlyFilter for state '{self.tag}' processing stream...", file=sys.stderr) # Optional debug
        for incoming_tag, line in lines:
            if "WARN" in line:
                # print(f"DEBUG: WarnOnlyFilter '{self.tag}' found WARN, yielding ('{self.next_tag}', '{line}')", file=sys.stderr) # Optional debug
                yield (self.next_tag, line)
            # else: line is dropped (not yielded)
        # print(f"DEBUG: WarnOnlyFilter for state '{self.tag}' finished stream.", file=sys.stderr) # Optional debug

