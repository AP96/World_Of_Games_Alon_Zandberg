# The Dockerfile is responsible for defining the environment
# and instructions to build the Docker image for your Flask application.
# The Flask application itself is defined in the Python files (main_score.py, score.py, etc.)
# which are copied into the Docker container and executed there.

# Use an official Python runtime as a parent image
FROM python:3.8-slim

# Set the working directory in the container
WORKDIR /app

COPY main_score.py /app/main_score.py
COPY score.py /app/score.py
COPY utils.py /app/utils.py
COPY requirements.txt /app/requirements.txt
COPY Scores.txt /app/Scores.txt

#Install packages specified in the requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Externalize 5000 available to the outside world
EXPOSE 5000

# Run main_score.py when the container launches
CMD ["python", "main_score.py"]

