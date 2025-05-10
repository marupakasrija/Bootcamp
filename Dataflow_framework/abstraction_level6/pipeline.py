# This is abstraction-level-6/pipeline.py
# Handles loading the State Transition configuration from YAML and creating the engine.

import yaml
import sys # Needed for sys.stderr
from typing import List, Dict, Any, Optional

# Import types using relative imports within the package
from .types import StateSystemConfig, StateProcessorFn, StateConfig, ProcessorDefinitionConfig, START_TAG, END_TAG

# Import the State Transition engine using a relative import
from .core.engine import StateTransitionEngine

# No direct processor loading here, the engine handles loading via core.utils

def load_state_system_config(config_path: str) -> StateSystemConfig:
    """
    Loads State Transition System configuration from a YAML file.

    Args:
        config_path: The path to the YAML configuration file.

    Returns:
        A dictionary representing the state system configuration.

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
        if not isinstance(config, dict) or 'states' not in config or not isinstance(config['states'], dict):
            raise ValueError("Config file must contain a top-level dictionary with a 'states' key containing a dictionary.")

        # TODO: Add more detailed validation for state definitions
        # - Each value in 'states' dictionary must be a dictionary with a 'type' (str) key

        # print(f"DEBUG: Successfully loaded config from {config_path}", file=sys.stderr) # Optional debug
        return config

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


def get_state_transition_engine_from_config(config_path: str) -> StateTransitionEngine:
    """
    Loads the State Transition configuration from a file and creates an engine instance.

    Args:
        config_path: The path to the YAML configuration file.

    Returns:
        An instance of StateTransitionEngine.

    Raises:
        Exception: If loading the config or initializing the engine fails.
    """
    print(f"Loading State Transition engine from config file: {config_path}", file=sys.stderr) # Informative print

    try:
        # Load the configuration structure from the YAML file.
        state_config = load_state_system_config(config_path)
        # Create an instance of the State Transition engine, passing the config.
        engine = StateTransitionEngine(state_config)
        # print("DEBUG: State Transition engine initialized successfully.", file=sys.stderr) # Optional debug
        return engine
    except Exception as e:
        print(f"Failed to initialize State Transition engine from config '{config_path}': {e}", file=sys.stderr)
        raise # Re-raise the exception to signal failure to the caller (main.py).

