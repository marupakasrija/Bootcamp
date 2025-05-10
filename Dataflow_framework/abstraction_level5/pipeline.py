# This is abstraction-level-5/pipeline.py
# Handles loading the DAG configuration from YAML and creating the execution engine.

import yaml
import sys # Needed for sys.stderr
from typing import List, Dict, Any, Optional

# Import types using relative imports within the package
from .types import DAGConfig, TaggedStreamProcessorFn, PipelineStepConfig, ProcessorConfig

# Import the DAG execution engine using a relative import
from .core.engine import DAGExecutionEngine

# Import the utility function for loading processor definitions
# from .core.utils import load_processor_definition # No longer needed here, engine loads definitions

def load_dag_config(config_path: str) -> DAGConfig:
    """
    Loads DAG configuration from a YAML file.

    Args:
        config_path: The path to the YAML configuration file.

    Returns:
        A dictionary representing the DAG configuration.

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
        if not isinstance(config, dict) or 'nodes' not in config or not isinstance(config['nodes'], list):
            raise ValueError("Config file must contain a top-level dictionary with a 'nodes' key containing a list.")
        if 'edges' not in config or not isinstance(config['edges'], dict):
             raise ValueError("Config file must contain an 'edges' key with a dictionary mapping node names to routing rules.")

        # TODO: Add more detailed validation for node and edge structures
        # - Each node in 'nodes' list must have 'name' (str) and 'type' (str)
        # - Each value in 'edges' dictionary must be a dictionary {tag: next_node_name}
        # - next_node_name must be a valid node name or the special FINAL_OUTPUT_TAG

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


def get_dag_engine_from_config(config_path: str) -> DAGExecutionEngine:
    """
    Loads the DAG configuration from a file and creates a DAG execution engine instance.

    Args:
        config_path: The path to the YAML DAG configuration file.

    Returns:
        An instance of DAGExecutionEngine.

    Raises:
        Exception: If loading the config or initializing the engine fails.
    """
    print(f"Loading DAG engine from config file: {config_path}", file=sys.stderr) # Informative print

    try:
        # Load the configuration structure from the YAML file.
        dag_config = load_dag_config(config_path)
        # Create an instance of the DAG execution engine, passing the config.
        engine = DAGExecutionEngine(dag_config)
        # print("DEBUG: DAG engine initialized successfully.", file=sys.stderr) # Optional debug
        return engine
    except Exception as e:
        print(f"Failed to initialize DAG engine from config '{config_path}': {e}", file=sys.stderr)
        raise # Re-raise the exception to signal failure to the caller (main.py).

