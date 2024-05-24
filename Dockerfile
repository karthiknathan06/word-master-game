# Use the official Python image from the Docker Hub
FROM python:3.9-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Create and set the working directory
WORKDIR /app

# Copy the requirements file into the container
COPY requirements.txt /app/

# Install the dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the entire project into the container
COPY . /app/

# Expose the port that the app runs on
EXPOSE 5000

# Run the application
CMD ["python", "app.py"]

# docker build -t spelling-bee-game .
# docker run -d -p 5001:5000 --name spelling-bee-game spelling-bee-game
