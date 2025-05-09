from typing import List
import sys
from .types import ProcessorFn
from .core import to_uppercase, to_snakecase

def get_pipeline(mode: str) -> List[ProcessorFn]:
    """Assembles a static pipeline based on the mode."""
    if mode == "uppercase":
        return [to_uppercase]
    elif mode == "snakecase":
        return [to_snakecase] 
    else:
        print(f"Warning: Unknown mode '{mode}'. Using empty pipeline.", file=sys.stderr)
        return []