# Use an official Python runtime as a parent image
FROM python:3.11-slim

# Set the working directory to /app
WORKDIR /app

# Install necessary system dependencies
RUN apt-get update -y && \
    apt-get install -y unzip libgl1-mesa-glx ffmpeg && \
    rm -rf /var/lib/apt/lists/*

# Install gdown
RUN pip install --no-cache-dir gdown

# Download and extract models
RUN gdown 1Jjsaixfk0n18xE1ks3SWEPD8Edozu0ZR -O /app/models.zip && \
    unzip /app/models.zip -d /app/app && \
    rm /app/models.zip

# Copy requirements file first to leverage Docker cache for dependencies
COPY requirements.txt /app/

# Install Python dependencies
RUN pip install --no-cache-dir --upgrade -r requirements.txt

# Copy the rest of the application code
COPY . /app

# Make port 8000 available to the world outside this container
EXPOSE 8000

# Run app.py when the container launches
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
