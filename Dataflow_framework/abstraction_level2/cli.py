import typer
from typing import Optional
import os
from dotenv import load_dotenv

load_dotenv()

app = typer.Typer()

# We define the app instance here to be imported by main.py