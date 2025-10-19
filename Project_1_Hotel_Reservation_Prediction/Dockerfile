# Use a lightweight Python image as the base for faster builds and smaller image size
FROM python:slim

# Set environment variables:
# - PYTHONDONTWRITEBYTECODE=1: Prevents Python from writing .pyc files to disk, keeping the container clean
# - PYTHONUNBUFFERED=1: Ensures Python outputs logs directly to the terminal (stdout/stderr) without buffering, useful for real-time logging
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

# Set the working directory inside the container to /app
WORKDIR /app

# Install system dependencies required by LightGBM (libgomp1 is needed for parallel processing)
RUN apt-get update && apt-get install -y --no-install-recommends \
    libgomp1 \
    build-essential \
    cmake \
    libssl-dev \
    libffi-dev \
    python3-dev \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Copy all files from the current directory on the host to the /app directory in the container
COPY . .

# Install the Python package in editable mode (-e .), allowing changes to the source code without reinstalling
RUN pip install --no-cache-dir -e .

# Run the training pipeline script to train the model before starting the application
RUN python pipeline/training_pipeline.py

# Expose port 5000 so the Flask app can be accessed from outside the container
EXPOSE 5000

# Set the default command to run the Flask application
CMD ["python", "application.py"]


