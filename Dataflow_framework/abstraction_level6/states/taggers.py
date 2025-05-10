# This is abstraction-level-6/states/taggers.py
# Contains state processors that primarily focus on changing tags for routing.

import sys # Needed for sys.stderr
from typing import Iterator, Optional, Tuple, Any, Dict
# Import base class and types using relative imports from the parent package (states)
from ..types import StateProcessor, ProcessorConfig, TaggedLine

class ContentRouter(StateProcessor):
    """
    A state processor that routes lines based on content matching rules.
    Emits a tag based on the first matching rule, or a default tag.
    """
    def __init__(self, tag: str, config: Optional[ProcessorConfig] = None):
        super().__init__(tag, config)
        # Config format: [{"tag": "tag_name", "contains": "text_to_match"}, ...]
        self.rules = self.config.get("rules", [])
        self.default_tag = self.config.get("default_tag", "default")
        # print(f"DEBUG: Initialized ContentRouter for state '{self.tag}' with default_tag='{self.default_tag}' and {len(self.rules)} rules", file=sys.stderr) # Optional debug


    def process(self, lines: Iterator[TaggedLine]) -> Iterator[TaggedLine]:
        """Processes lines and yields (next_tag, line) based on rules."""
        # print(f"DEBUG: ContentRouter for state '{self.tag}' processing stream...", file=sys.stderr) # Optional debug
        for incoming_tag, line in lines:
            emitted = False
            # Check each rule in order
            for rule in self.rules:
                next_tag = rule.get("tag", self.default_tag)
                contains_text = rule.get("contains")
                if contains_text is not None and contains_text in line:
                    # Found a match, yield with the rule's tag
                    # print(f"DEBUG: ContentRouter '{self.tag}' matched rule for tag '{next_tag}', yielding ('{next_tag}', '{line}')", file=sys.stderr) # Optional debug
                    yield (next_tag, line)
                    emitted = True
                    # Optional: break after first match, or continue for multiple tags
                    # For simple routing, break is typical.
                    break
            if not emitted:
                # No rules matched, yield with the default tag
                # print(f"DEBUG: ContentRouter '{self.tag}' no rule matched, yielding ('{self.default_tag}', '{line}')", file=sys.stderr) # Optional debug
                yield (self.default_tag, line)
        # print(f"DEBUG: ContentRouter for state '{self.tag}' finished stream.", file=sys.stderr) # Optional debug

