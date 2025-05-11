# Makefile for Routing Engine

# Define variables
PYTHON = python
PIP = $(PYTHON) -m pip
WATCH_DIR = watch_dir
SINGLE_FILE = sample_general.txt # Default file for single run
DOCKER_IMAGE_NAME = routing-engine

.PHONY: install run-watch run-single clean docker-build docker-run help

# Default target
all: help

# Install dependencies
install:
	@echo "Installing Python dependencies..."
	$(PIP) install -r requirements.txt
	@echo "Dependencies installed."

# Run the engine in watch mode
run-watch: install
	@echo "Starting routing engine in watch mode..."
	$(PYTHON) main.py --watch --dashboard-port 8000 --dashboard-host 127.0.0.1

# Run the engine in single file mode
# Usage: make run-single FILE=path/to/your/file.txt
run-single: install
	@echo "Starting routing engine in single file mode for $(FILE)..."
	$(PYTHON) main.py --input $(FILE) --dashboard-port 8000 --dashboard-host 127.0.0.1

# Clean up generated files and directories
clean:
	@echo "Cleaning up..."
	@find . -type d -name "__pycache__" -exec rm -rf {} + || true
	@find . -type d -name ".pytest_cache" -exec rm -rf {} + || true
	@rm -rf $(WATCH_DIR)/unprocessed/* || true
	@rm -rf $(WATCH_DIR)/underprocess/* || true
	# Optionally keep processed files, or uncomment below to remove them too
	# @rm -rf $(WATCH_DIR)/processed/* || true
	@echo "Cleanup complete."

# Build the Docker image
docker-build:
	@echo "Building Docker image $(DOCKER_IMAGE_NAME)..."
	docker build -t $(DOCKER_IMAGE_NAME) .
	@echo "Docker image built."

# Run the Docker container in watch mode
# Mounts the watch_dir volume for file persistence
docker-run: docker-build
	@echo "Running Docker container in watch mode..."
	@echo "Access dashboard at http://127.0.0.1:8000/docs"
	docker run -d --rm \
		-p 8000:8000 \
		-v $(shell pwd)/$(WATCH_DIR):/app/$(WATCH_DIR) \
		--name $(DOCKER_IMAGE_NAME)-container \
		$(DOCKER_IMAGE_NAME) \
		--watch --dashboard-host 0.0.0.0 # Use 0.0.0.0 inside container

# Helper target for displaying help
help:
	@echo "Usage: make [target]"
	@echo ""
	@echo "Targets:"
	@echo "  install       Install Python dependencies."
	@echo "  run-watch     Run the engine in continuous watch mode."
	@echo "  run-single    Run the engine in single file mode. Use FILE=<path> (e.g., make run-single FILE=my_file.txt)."
	@echo "  clean         Clean up cache directories and watch_dir contents (keeps processed)."
	@echo "  docker-build  Build the Docker image."
	@echo "  docker-run    Build and run the Docker container in watch mode."
	@echo "  help          Display this help message."

