# This is abstraction-level-5/core/utils.py
# Contains helper functions for the core execution engine.

import sys # Needed for sys.stderr
import importlib # Needed for dynamic imports
from typing import Iterator, Optional, Any, Dict, Callable, Tuple
# Import types using relative imports from the parent package (core)
# Need to go up one level to abstraction-level-5, then down into types
from ..types import TaggedStreamProcessor, ProcessorConfig, TaggedLine, TaggedStreamProcessorFn, StreamProcessor # StreamProcessor kept for potential wrapping if needed

# --- Helper to instantiate processor classes ---
def instantiate_processor(processor_class, name: str, config: Optional[ProcessorConfig] = None) -> TaggedStreamProcessor:
    """Instantiates a TaggedStreamProcessor class, passing name and configuration."""
    try:
        # Check if it's a class and a subclass of TaggedStreamProcessor (good practice)
        if not isinstance(processor_class, type) or not issubclass(processor_class, TaggedStreamProcessor):
             raise TypeError(f"Expected a TaggedStreamProcessor class, but got {type(processor_class)}")

        # Instantiate the class, passing the name and config
        instance = processor_class(name=name, config=config)
        # print(f"DEBUG: Instantiated processor class: {processor_class.__name__} with name '{name}'", file=sys.stderr) # Optional debug
        return instance
    except Exception as e:
        print(f"Error instantiating processor class {getattr(processor_class, '__name__', 'anonymous')} with name '{name}': {e}", file=sys.stderr)
        raise # Re-raise the exception


# --- Helper to get a TaggedStreamProcessorFn from a definition ---
def get_tagged_stream_processor(processor_definition, name: str, config: Optional[ProcessorConfig] = None) -> TaggedStreamProcessorFn:
    """
    Takes a processor definition (a TaggedStreamProcessor class or a
    Iterator[str] -> Iterator[TaggedLine] function) and returns a
    TaggedStreamProcessorFn.

    Args:
        processor_definition: The processor class or function.
        name: The name of the node in the DAG (passed to class constructor).
        config: Optional configuration dictionary for class-based processors.

    Returns:
        A callable function that takes an iterator and yields (tag, line) tuples.

    Raises:
        TypeError: If the definition is not a supported type.
    """
    # Check if it's a TaggedStreamProcessor class
    if isinstance(processor_definition, type) and issubclass(processor_definition, TaggedStreamProcessor):
        # Instantiate the class and return its process method
        instance = instantiate_processor(processor_definition, name=name, config=config)
        return instance.process
    # Check if it's a callable (assume it matches TaggedStreamProcessorFn signature)
    elif callable(processor_definition):
         # Assume the function already matches the signature Iterator[str] -> Iterator[TaggedLine]
         # TODO: Could add a check here to verify the signature.
         # If it does, return it directly.
         # print(f"DEBUG: Using function-based processor: {getattr(processor_definition, '__name__', 'anonymous')}", file=sys.stderr) # Optional debug
         return processor_definition
    else:
        raise TypeError(f"Processor definition must be a callable function or a TaggedStreamProcessor class, got {type(processor_definition)}")

# --- Helper to dynamically load processor definition (function or class) ---
# Moved from pipeline.py to core/utils.py for better separation
def load_processor_definition(dotted_path: str):
    """
    Dynamically loads a processor definition (a function or a class) from a
    dotted import path string, resolving the path relative to the root package.

    Includes the fallback import logic from L3/L4.

    Args:
        dotted_path: The dotted path to the function or class
                     (e.g., 'processors.upper.UppercaseProcessor', 'processors.stateful.LineCounterProcessor').
                     This path is relative to the root of the package containing this module.

    Returns:
        The loaded callable function or class.

    Raises:
        ImportError: If the module or name cannot be found.
        Exception: For other unexpected errors during loading.
    """
    module = None
    definition = None
    module_name = None
    name = None

    try:
        # Split the path into module name and definition name (function or class name).
        module_name, name = dotted_path.rsplit('.', 1)

        # --- DEBUG PRINT ---
        # print(f"DEBUG: load_processor_definition received dotted_path='{dotted_path}'", file=sys.stderr) # Optional debug
        # print(f"DEBUG: Split into module_name='{module_name}' and name='{name}'", file=sys.stderr) # Optional debug
        # --- END DEBUG PRINT ---

        # --- Attempt 1: Dynamic import relative to the root package ---
        # Get the root package name from the current module's __package__
        # If __package__ is 'abstraction_level5.core', root_package is 'abstraction_level5'
        root_package = __package__.split('.')[0] if __package__ else None

        if root_package: # Check if running within a package context
            try:
                # Construct the full absolute import path from the root package
                full_dotted_path = f"{root_package}.{dotted_path}"
                # --- DEBUG PRINT ---
                print(f"DEBUG: Attempt 1: Dynamically importing using full dotted path='{full_dotted_path}'", file=sys.stderr)
                # --- END DEBUG PRINT ---
                # Perform the import using the full absolute path
                module = importlib.import_module(full_dotted_path)
                # --- DEBUG PRINT ---
                print(f"DEBUG: Attempt 1: Successfully imported module: {module.__name__}", file=sys.stderr)
                # --- END DEBUG PRINT ---

            except ImportError as e:
                # If the first attempt fails, store the error and re-raise later if needed
                # print(f"DEBUG: Attempt 1 (full path import) failed: {e}", file=sys.stderr) # Keep this debug if needed
                module = None # Reset module to ensure we raise the correct error later


        # --- Fallback: If not in a package context or first attempt failed, try absolute import directly ---
        # This case might be less relevant when consistently using 'python -m',
        # but kept for robustness or if the dotted_path was intended as absolute.
        if module is None:
             try:
                 # --- DEBUG PRINT ---
                 print(f"DEBUG: Attempt 2: Dynamically importing using dotted path='{dotted_path}' (absolute import)", file=sys.stderr)
                 # --- END DEBUG PRINT ---
                 module = importlib.import_module(dotted_path)
                 # --- DEBUG PRINT ---
                 print(f"DEBUG: Attempt 2: Successfully imported module: {module.__name__}", file=sys.stderr)
                 # --- END DEBUG PRINT ---
             except ImportError as e:
                 # If absolute import also fails, re-raise the original relative import error if available, or this one.
                 # print(f"DEBUG: Attempt 2 (absolute import) failed: {e}", file=sys.stderr) # Keep this debug if needed
                 # Re-raise with a more informative message
                 if root_package:
                     raise ImportError(f"Could not import module '{dotted_path}' relative to root package '{root_package}' or using absolute path") from e
                 else:
                     raise ImportError(f"Could not import module '{dotted_path}' using absolute path") from e


        # --- If module was successfully imported ---
        if module:
            # --- DEBUG PRINT ---
            # print(f"DEBUG: Attempting to get attribute '{name}' from module '{module.__name__}'", file=sys.stderr) # Optional debug
            # --- END DEBUG PRINT ---

            # Get the function or class object from the module.
            definition = getattr(module, name)

            # print(f"DEBUG: Successfully loaded definition: {dotted_path}", file=sys.stderr) # Optional debug
            return definition
        else:
             # This else should theoretically not be reached if importlib raises ImportError,
             # but as a fallback, raise a generic error.
             raise ImportError(f"Failed to load module for path '{dotted_path}' - Unknown Reason")


    except ImportError:
        # Catch import errors (module or name not found) that weren't handled above.
        # The more specific error message should have been printed by the attempts above.
        # print(
        #     f"Error: Could not import module or find name at path: '{dotted_path}'. "
        #     f"Please check the path in your config file.",
        #     file=sys.stderr
        # ) # Error message is already printed by the attempts above
        raise # Re-raise the exception.
    except AttributeError:
        # Catch attribute errors (name not found in module).
        print(
            f"Error: Could not find name '{name}' in module '{module_name}' at path: '{dotted_path}'. "
            f"Please check the path in your config file.",
            file=sys.stderr
        )
        raise # Re-raise the exception.
    except Exception as e:
        # Catch any other unexpected errors during the loading process.
        print(f"An unexpected error occurred loading definition '{dotted_path}': {e}", file=sys.stderr)
        raise # Re-raise the exception.

