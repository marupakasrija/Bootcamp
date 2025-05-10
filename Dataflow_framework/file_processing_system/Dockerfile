# Use an official Python runtime as a parent image
FROM python@sha256:digest-value

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file into the container
COPY requirements.txt .

# Install any needed dependencies specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code into the container
COPY . .

# Create the watch_dir structure inside the container
RUN mkdir -p watch_dir/unprocessed watch_dir/processed watch_dir/error

# Make the watch_dir accessible/writable (optional, depending on user/permissions)
# RUN chmod -R 777 watch_dir

# Expose the port the FastAPI app runs on
EXPOSE 8000

# Run the main.py script when the container launches
# Default command is to run in watch mode
CMD ["python", "main.py", "--watch"]