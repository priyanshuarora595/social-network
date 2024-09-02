# Use the official Python image as the base image
FROM python:3.9-slim

# Set environment variables to prevent Python from writing .pyc files to disc
# and to ensure that Python output is sent straight to the terminal (i.e., not buffered)
ENV PYTHONUNBUFFERED 1

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file into the container
COPY requirements.txt /app/


# Copy the entire project into the container
COPY . /app/
# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Expose the port that the application will run on
EXPOSE 8000

# Command to run the application
CMD ["python", "manage.py", "runserver","0.0.0.0:8000"]