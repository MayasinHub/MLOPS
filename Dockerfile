# Use an official Python runtime as a parent image
FROM python:3.9-slim

# Set the working directory
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Expose ports for the FastAPI and Streamlit apps
EXPOSE $PORT

# Command to run both FastAPI and Streamlit
CMD gunicorn --workers=4 --bind 0.0.0.0:$PORT main:app
