# # Use an official Python runtime as a parent image
# FROM python:3.9-slim

# # Set the working directory inside the container
# WORKDIR /app

# # Install system dependencies
# RUN apt-get update && apt-get install -y \
#     gcc \
#     libpq-dev \
#     && apt-get clean

# # Install Python dependencies
# COPY requirements.txt /app/
# RUN pip install --no-cache-dir -r requirements.txt

# # Copy the current directory contents into the container
# COPY . /app/

# # Expose the port the app runs on
# EXPOSE 8000

# # Define environment variable
# ENV PYTHONUNBUFFERED 1

# # Run Django's development server
# CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]


# Use a smaller official Python image
FROM python:3.9-slim

# Set environment variables early to reduce image size
ENV PYTHONDONTWRITEBYTECODE=1 PYTHONUNBUFFERED=1


# Set working directory
WORKDIR /app

# Install only essential system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy project files
COPY . .

# Expose the port your Django app runs on
EXPOSE 8000

# Run the application
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
