import yaml
import importlib
import sys 
from typing import List, Dict, Any
from .types import ProcessorFn, PipelineStepConfig

def load_processor(dotted_path: str) -> ProcessorFn:
    """
    Dynamically loads a processor function from a dotted import path string,
    resolving the path relative to the current package.

    Args:
        dotted_path: The dotted path to the function (e.g., 'processors.upper.to_uppercase').
                     This path is relative to the root of the package containing this module.

    Returns:
        The loaded callable processor function.

    Raises:
        ImportError: If the module or function cannot be found.
        TypeError: If the loaded object is not callable.
        Exception: For other unexpected errors during loading.
    """
    module = None
    processor_fn = None
    module_name = None
    func_name = None

    try:
        # Split the path into module name and function name.
        # Example: 'processors.upper.to_uppercase' -> module_name='processors.upper', func_name='to_uppercase'
        module_name, func_name = dotted_path.rsplit('.', 1)

        # --- DEBUG PRINT ---
        # print(f"DEBUG: load_processor received dotted_path='{dotted_path}'", file=sys.stderr)
        # print(f"DEBUG: Split into module_name='{module_name}' and func_name='{func_name}'", file=sys.stderr)
        # --- END DEBUG PRINT ---

        # --- Attempt 1: Dynamic import relative to the current package ---
        # This is the intended way when running with python -m
        if __package__: # Check if running within a package context
            try:
                # --- DEBUG PRINT ---
                print(f"DEBUG: Attempt 1: Dynamically importing module '{module_name}' relative to package='{__package__}'", file=sys.stderr)
                # --- END DEBUG PRINT ---
                module = importlib.import_module(module_name, package=__package__)
                # --- DEBUG PRINT ---
                print(f"DEBUG: Attempt 1: Successfully imported module: {module.__name__}", file=sys.stderr)
                # --- END DEBUG PRINT ---

            except ImportError as e:
                # If relative import fails, store the error and try absolute import
                # print(f"DEBUG: Attempt 1 (relative import) failed: {e}", file=sys.stderr) # Keep this debug if needed
                module = None # Reset module to ensure we try the next step


        # --- Attempt 2: Dynamic import using the full absolute path ---
        # Construct the full absolute path: current_package_name.module_name
        # This might work if the relative import is somehow misbehaving.
        if module is None and __package__: # Only try if relative failed and we know the package
             full_module_path = f"{__package__}.{module_name}"
             try:
                 # --- DEBUG PRINT ---
                 print(f"DEBUG: Attempt 2: Dynamically importing module using full path='{full_module_path}'", file=sys.stderr)
                 # --- END DEBUG PRINT ---
                 module = importlib.import_module(full_module_path)
                 # --- DEBUG PRINT ---
                 print(f"DEBUG: Attempt 2: Successfully imported module: {module.__name__}", file=sys.stderr)
                 # --- END DEBUG PRINT ---
             except ImportError as e:
                 # If absolute import also fails, re-raise the original relative import error if available, or this one.
                 # print(f"DEBUG: Attempt 2 (absolute import) failed: {e}", file=sys.stderr) # Keep this debug if needed
                 # Re-raise with a more informative message
                 raise ImportError(f"Could not import module '{module_name}' relative to '{__package__}' or using absolute path '{full_module_path}' for path '{dotted_path}'") from e
        elif module is None: # If not running in a package context (__package__ is None)
             # This case shouldn't happen with python -m, but handle defensively
             try:
                 # --- DEBUG PRINT ---
                 # print(f"DEBUG: Attempting absolute import for module '{module_name}' (not in package context)", file=sys.stderr) # Keep this debug if needed
                 # --- END DEBUG PRINT ---
                 module = importlib.import_module(module_name)
                 # --- DEBUG PRINT ---
                 # print(f"DEBUG: Successfully imported module: {module.__name__}", file=sys.stderr) # Keep this debug if needed
                 # --- END DEBUG PRINT ---
             except ImportError as e:
                 # print(f"DEBUG: Absolute import failed: {e}", file=sys.stderr) # Keep this debug if needed
                 raise ImportError(f"Could not import module '{module_name}' for path '{dotted_path}'") from e


        # --- If module was successfully imported by either attempt ---
        if module:
            # --- DEBUG PRINT ---
            # print(f"DEBUG: Attempting to get attribute '{func_name}' from module '{module.__name__}'", file=sys.stderr) # Keep this debug if needed
            # --- END DEBUG PRINT ---

            # Get the function object from the module.
            processor_fn = getattr(module, func_name)

            # Basic check to ensure the loaded object is callable (a function or method).
            if not callable(processor_fn):
                 raise TypeError(f"Object at path '{dotted_path}' is not callable.")

            # print(f"DEBUG: Successfully loaded processor: {dotted_path}") # Optional debug print
            return processor_fn
        else:
             # This else should theoretically not be reached if importlib raises ImportError,
             # but as a fallback, raise a generic error.
             raise ImportError(f"Failed to load module for path '{dotted_path}' - Unknown Reason")


    except ImportError:
        # Catch import errors (module or function not found) that weren't handled above.
        # The more specific error message should have been printed by the attempts above.
        # print(
        #     f"Error: Could not import module or find function at path: '{dotted_path}'. "
        #     f"Please check the path in your config file.",
        #     file=sys.stderr
        # ) # Error message is already printed by the attempts above
        raise # Re-raise the exception.
    except AttributeError:
        # Catch attribute errors (function name not found in module).
        print(
            f"Error: Could not find function '{func_name}' in module '{module_name}' at path: '{dotted_path}'. "
            f"Please check the path in your config file.",
            file=sys.stderr
        )
        raise # Re-raise the exception.
    except Exception as e:
        # Catch any other unexpected errors during the loading process.
        print(f"An unexpected error occurred loading processor '{dotted_path}': {e}", file=sys.stderr)
        raise # Re-raise the exception.


def load_pipeline_config(config_path: str) -> List[PipelineStepConfig]:
    """
    Loads pipeline configuration from a YAML file.

    Args:
        config_path: The path to the YAML configuration file.

    Returns:
        A list of pipeline step configurations (dictionaries).

    Raises:
        FileNotFoundError: If the config file does not exist.
        yaml.YAMLError: If the YAML file is invalid.
        ValueError: If the config structure is incorrect.
        Exception: For other unexpected errors.
    """
    try:
        with open(config_path, 'r') as f:
            config = yaml.safe_load(f)

        # Validate the basic structure of the config file.
        if not isinstance(config, dict) or 'pipeline' not in config or not isinstance(config['pipeline'], list):
            raise ValueError("Config file must contain a top-level dictionary with a 'pipeline' key containing a list.")

        # Validate each step in the pipeline list.
        pipeline_steps = config['pipeline']
        for i, step in enumerate(pipeline_steps):
            if not isinstance(step, dict) or 'type' not in step or not isinstance(step['type'], str):
                 raise ValueError(f"Pipeline step {i} is invalid. Must be a dictionary with a string 'type' key.")

        # print(f"DEBUG: Successfully loaded config from {config_path}") # Optional debug print
        return pipeline_steps

    except FileNotFoundError:
        print(f"Error: Config file not found at '{config_path}'. Please check the path.", file=sys.stderr)
        raise
    except yaml.YAMLError as e:
        print(f"Error parsing YAML config file '{config_path}': {e}", file=sys.stderr)
        raise
    except ValueError as e:
        print(f"Invalid config file format in '{config_path}': {e}", file=sys.stderr)
        raise
    except Exception as e:
        print(f"An unexpected error occurred loading config '{config_path}': {e}", file=sys.stderr)
        raise


def get_pipeline_from_config(config_path: str) -> List[ProcessorFn]:
    """
    Loads the pipeline configuration from a file and dynamically loads
    the corresponding processor functions.

    Args:
        config_path: The path to the YAML pipeline configuration file.

    Returns:
        A list of callable ProcessorFn functions representing the pipeline.

    Raises:
        Exception: If loading the config or any processor fails.
    """
    print(f"Loading pipeline from config file: {config_path}") # Informative print

    # Load the configuration structure from the YAML file.
    pipeline_config = load_pipeline_config(config_path)

    # List to store the loaded processor functions.
    processors: List[ProcessorFn] = []

    # Iterate through each step defined in the config.
    for step_config in pipeline_config:
        # The 'type' key holds the dotted import path.
        processor_path = step_config['type']

        try:
            # Dynamically load the processor function using its dotted path.
            processor_fn = load_processor(processor_path)
            # Add the loaded function to our list of processors.
            processors.append(processor_fn)
            # print(f"DEBUG: Added processor '{processor_path}' to pipeline.") # Optional debug print

        except Exception as e:
            # If loading any single processor fails, print an error and stop
            # loading the rest of the pipeline.
            print(f"Failed to load processor '{processor_path}'. Aborting pipeline loading.", file=sys.stderr)
            raise # Re-raise the exception to signal failure to the caller (main.py).

    print(f"Pipeline loaded successfully with {len(processors)} steps.") # Informative print
    return processors
