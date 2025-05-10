.PHONY: build-docker run run-local run-docker build-package publish-package clean help dirs

# --- Variables ---
IMAGE_NAME = file-processing-system
PACKAGE_DIR = dist
# --- End Variables ---

# Default target when you just type 'make'
all: help

help:
    @echo "Usage: make [target]"
    @echo ""
    @echo "Targets:"
    @echo "  help             Show this help message."
    @echo "  dirs             Create the necessary watch directories."
    @echo "  install          Install Python dependencies (pip install -r requirements.txt)."
    @echo "  run-local        Run the application directly using Python (default: watch mode)."
    @echo "  run-docker       Build and run the application using Docker (watch mode)."
    @echo "  build-docker     Build the Docker image for the application."
    @echo "  build-package    Build the Python distribution package."
    @echo "  publish-package  Publish the package to PyPI (requires twine)."
    @echo "  clean            Remove build artifacts and cache files."
    @echo ""
    @echo "Example: make run-local ARGS='--input path/to/file.txt'"
    @echo "Example: make run-docker"

# Target to create directories
dirs:
    @echo "Creating watch directories..."
    mkdir -p watch_dir/unprocessed watch_dir/processed watch_dir/error
    @echo "Directories created."

# Target to install dependencies
install:
    @echo "Installing Python dependencies..."
    pip install -r requirements.txt
    @echo "Dependencies installed."

# Target to run locally
# Accepts optional ARGS variable, e.g., make run-local ARGS="--input my_file.txt"
run-local: dirs install
    @echo "Running application locally..."
    python main.py $(ARGS)

# Target to build and run with Docker
run-docker: build-docker dirs
    @echo "Running application in Docker..."
    # Mount the local watch_dir volume to /app/watch_dir in the container
    # Map port 8000 from the container to port 8000 on the host
    docker run --rm -p 8000:8000 -v ${PWD}/watch_dir:/app/watch_dir $(IMAGE_NAME) $(ARGS)

# Target to build the Docker image
build-docker:
    @echo "Building Docker image $(IMAGE_NAME)..."
    docker build -t $(IMAGE_NAME) .
    @echo "Docker image $(IMAGE_NAME) built."

# Target to build the Python package
# Assumes you have a pyproject.toml or setup.py
build-package:
    @echo "Building Python package..."
    # Ensure build and twine are installed (add to requirements.txt or install here)
    pip install build twine
    python -m build
    @echo "Package built in $(PACKAGE_DIR)/"

# Target to publish the Python package
publish-package: build-package
    @echo "Publishing package..."
    # Requires TWINE_USERNAME and TWINE_PASSWORD environment variables or ~/.pypirc
    twine upload $(PACKAGE_DIR)/*
    @echo "Package published."

# Target to clean up build artifacts
clean:
    @echo "Cleaning build artifacts..."
    rm -rf build $(PACKAGE_DIR) *.egg-info
    find . -name "__pycache__" -type d -exec rm -r {} + || true # Ignore errors if no __pycache__
    find . -name "*.pyc" -delete || true # Ignore errors if no .pyc files
    @echo "Clean complete."