# This is abstraction-level-8/cli.py
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

# Command definitions are typically defined in main.py after importing this 'app' instance.
# The --watch-dir and --trace flags are added in main.py's command definition.
