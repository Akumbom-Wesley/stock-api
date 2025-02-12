# Use an official Python runtime as a parent image
FROM python:3.9-slim

# Set environment variables
ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1

# Install system dependencies (build-essential, gcc, etc.)
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    gcc \
    libpq-dev \
    python3-dev \
    && rm -rf /var/lib/apt/lists/*

# Set the working directory in the container
WORKDIR /app

# Copy requirements.txt to leverage Docker cache
COPY requirements.txt /app/

# Upgrade pip and install Python dependencies
RUN pip install --upgrade pip && \
    pip install -r requirements.txt

# Copy the rest of the project code into the container
COPY . /app/

# Expose the port your Django app runs on (default 8000)
EXPOSE 8000

# Run migrations and start the Gunicorn server.
# Replace "stock_api" with your actual project name if different.
CMD ["sh", "-c", "python manage.py migrate && gunicorn stock_api.wsgi:application --bind 0.0.0.0:$PORT"]
