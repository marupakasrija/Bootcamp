# Dockerfile for Routing Engine

# Use a lightweight Python base image
FROM python:3.12-slim

# Set the working directory inside the container
WORKDIR /app

# Copy the requirements file and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code
COPY . .

# Create the watch directories
RUN mkdir -p watch_dir/unprocessed \
           watch_dir/underprocess \
           watch_dir/processed

# Expose the port the FastAPI server will run on
EXPOSE 8000

# Command to run the application in watch mode by default
# Use --dashboard-host 0.0.0.0 to make the dashboard accessible outside the container
CMD ["python", "main.py", "--watch", "--dashboard-host", "0.0.0.0", "--dashboard-port", "8000"]

# Note: For single file mode with Docker, you would typically
# use a different command when running the container, e.g.:
# docker run --rm -v /path/on/host/my_file.txt:/app/my_file.txt routing-engine --input my_file.txt
# Or build a separate image/entrypoint for single file processing.
