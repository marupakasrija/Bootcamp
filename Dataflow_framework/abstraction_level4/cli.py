# This is abstraction-level-4/cli.py
# Handles the command-line interface setup using Typer.

import typer
import os
from dotenv import load_dotenv

# Load environment variables from a .env file.
# This allows setting default options.
load_dotenv()

# Create a Typer application instance.
# This instance will be imported by main.py to define commands.
app = typer.Typer()

# Command definitions (like the 'process_file' command) are typically
# defined in main.py after importing this 'app' instance to avoid
# circular import dependencies with other modules like core and pipeline
# that main.py also needs to import.
