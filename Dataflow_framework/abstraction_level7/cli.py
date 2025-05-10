# This is abstraction-level-7/cli.py
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