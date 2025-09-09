# Use a smaller official Python image
FROM python:3.9-slim

# Set environment variables early to reduce image size
ENV PYTHONDONTWRITEBYTECODE=1 PYTHONUNBUFFERED=1


# Set working directory
WORKDIR /app

# Install only essential system dependencies

# Install build tools for pip packages
RUN apt-get update && apt-get install -y --no-install-recommends gcc

# Install Python dependencies
COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

# Clean up build tools and apt cache after pip install
RUN apt-get remove -y gcc && apt-get autoremove -y && apt-get clean && rm -rf /var/lib/apt/lists/*

# Copy project files
COPY . .

# Create a non-root user for security
RUN adduser --disabled-password --gecos '' appuser && chown -R appuser:appuser /app
USER appuser

# Expose the port your Django app runs on
EXPOSE 8000

# Collect static files
RUN python manage.py collectstatic --noinput

# Run the application with Gunicorn using configuration file
CMD ["gunicorn", "--config", "gunicorn.conf.py", "slideshare_project.wsgi:application"]
