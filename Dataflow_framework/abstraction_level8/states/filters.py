# This is abstraction-level-8/states/filters.py
# Contains filtering state processors. Adapted for TracedLine.

import sys # Needed for sys.stderr
from typing import Iterator, Optional, Tuple, Any, Dict
# Import base class and types using relative imports from the parent package (states)
from ..types import StateProcessor, ProcessorConfig, TracedLine

class ErrorOnlyFilter(StateProcessor):
    """
    A state processor that only yields lines containing "ERROR", with a fixed next tag.
    Lines not containing "ERROR" are dropped (not yielded). Handles TracedLine.
    """
    def __init__(self, tag: str, config: Optional[ProcessorConfig] = None):
        super().__init__(tag, config)
        self.next_tag = self.config.get("next_tag", "error_processed")
        # print(f"DEBUG: Initialized ErrorOnlyFilter for state '{self.tag}' with next_tag='{self.next_tag}'", file=sys.stderr) # Optional debug)


    def process(self, lines: Iterator[TracedLine]) -> Iterator[TracedLine]:
        """
        Processes lines received (as TracedLine), yields only error lines
        with next_tag and updated_history.
        """
        # print(f"DEBUG: ErrorOnlyFilter for state '{self.tag}' processing stream...", file=sys.stderr) # Optional debug)
        for line_id, incoming_tag, line_content, history in lines:
            if "ERROR" in line_content:
                updated_history = history + [self.tag] # Add current state to history
                # print(f"DEBUG: ErrorOnlyFilter '{self.tag}' found ERROR, yielding ('{line_id}', '{self.next_tag}', '{line_content}', {updated_history})", file=sys.stderr) # Optional debug)
                yield (line_id, self.next_tag, line_content, updated_history)
            # else: line is dropped (not yielded)
        # print(f"DEBUG: ErrorOnlyFilter for state '{self.tag}' finished stream.", file=sys.stderr) # Optional debug)


class WarnOnlyFilter(StateProcessor):
    """
    A state processor that only yields lines containing "WARN", with a fixed next tag.
    Lines not containing "WARN" are dropped (not yielded). Handles TracedLine.
    """
    def __init__(self, tag: str, config: Optional[ProcessorConfig] = None):
        super().__init__(tag, config)
        self.next_tag = self.config.get("next_tag", "warn_processed")
        # print(f"DEBUG: Initialized WarnOnlyFilter for state '{self.tag}' with next_tag='{self.next_tag}'", file=sys.stderr) # Optional debug)


    def process(self, lines: Iterator[TracedLine]) -> Iterator[TracedLine]:
        """
        Processes lines received (as TracedLine), yields only warn lines
        with next_tag and updated_history.
        """
        # print(f"DEBUG: WarnOnlyFilter for state '{self.tag}' processing stream...", file=sys.stderr) # Optional debug)
        for line_id, incoming_tag, line_content, history in lines:
            if "WARN" in line_content:
                updated_history = history + [self.tag] # Add current state to history
                # print(f"DEBUG: WarnOnlyFilter '{self.tag}' found WARN, yielding ('{line_id}', '{self.next_tag}', '{line_content}', {updated_history})", file=sys.stderr) # Optional debug)
                yield (line_id, self.next_tag, line_content, updated_history)
            # else: line is dropped (not yielded)
        # print(f"DEBUG: WarnOnlyFilter for state '{self.tag}' finished stream.", file=sys.stderr) # Optional debug)

