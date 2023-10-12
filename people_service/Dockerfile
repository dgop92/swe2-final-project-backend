# Use the official Python image as the parent image
FROM python:3.10-slim-buster

# Set the working directory to /app
WORKDIR /app

# Copy the requirements file into the container and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code into the container
COPY . .

# Expose port 8000 for the FastAPI server
EXPOSE 8000

# Start the the default FastAPI server
CMD ["uvicorn", "services.read_service:app", "--host", "0.0.0.0", "--port", "8000"]
