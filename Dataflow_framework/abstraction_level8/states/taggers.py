# This is abstraction-level-8/states/taggers.py
# Contains state processors that primarily focus on changing tags for routing. Adapted for TracedLine.

import sys # Needed for sys.stderr
from typing import Iterator, Optional, Tuple, Any, Dict
# Import base class and types using relative imports from the parent package (states)
from ..types import StateProcessor, ProcessorConfig, TracedLine

class ContentRouter(StateProcessor):
    """
    A state processor that routes lines based on content matching rules.
    Emits a tag based on the first matching rule, or a default tag. Handles TracedLine.
    """
    def __init__(self, tag: str, config: Optional[ProcessorConfig] = None):
        super().__init__(tag, config)
        # Config format: [{"tag": "tag_name", "contains": "text_to_match"}, ...]
        self.rules = self.config.get("rules", [])
        self.default_tag = self.config.get("default_tag", "default")
        # print(f"DEBUG: Initialized ContentRouter for state '{self.tag}' with default_tag='{self.default_tag}' and {len(self.rules)} rules", file=sys.stderr) # Optional debug)


    def process(self, lines: Iterator[TracedLine]) -> Iterator[TracedLine]:
        """
        Processes lines received (as TracedLine) and yields (id, next_tag, line, updated_history)
        based on rules.
        """
        # print(f"DEBUG: ContentRouter for state '{self.tag}' processing stream...", file=sys.stderr) # Optional debug)
        for line_id, incoming_tag, line_content, history in lines:
            emitted = False
            updated_history = history + [self.tag] # Add current state to history
            # Check each rule in order
            for rule in self.rules:
                next_tag = rule.get("tag", self.default_tag)
                contains_text = rule.get("contains")
                if contains_text is not None and contains_text in line_content:
                    # Found a match, yield with the rule's tag
                    # print(f"DEBUG: ContentRouter '{self.tag}' matched rule for tag '{next_tag}', yielding ('{line_id}', '{next_tag}', '{line_content}', {updated_history})", file=sys.stderr) # Optional debug)
                    yield (line_id, next_tag, line_content, updated_history)
                    emitted = True
                    # Optional: break after first match, or continue for multiple tags
                    # For simple routing, break is typical.
                    break
            if not emitted:
                # No rules matched, yield with the default tag
                # print(f"DEBUG: ContentRouter '{self.tag}' no rule matched, yielding ('{self.default_tag}', '{line_content}', {updated_history})", file=sys.stderr) # Optional debug)
                yield (line_id, self.default_tag, line_content, updated_history)
        # print(f"DEBUG: ContentRouter for state '{self.tag}' finished stream.", file=sys.stderr) # Optional debug)

