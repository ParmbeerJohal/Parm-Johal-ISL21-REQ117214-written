# Use a Python image
FROM python:3.13.0-slim

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file into the container
COPY docs/requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the application code into the container
COPY src/ ./src/
COPY main.py .

# Expose the MQTT default port
EXPOSE 1883

# Using ENTRYPOINT to include topic ID parameter
ENTRYPOINT ["python", "main.py"]
