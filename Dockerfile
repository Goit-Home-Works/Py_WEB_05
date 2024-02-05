# Use an official Python runtime as a parent image
FROM python:3.12-slim

# Set the working directory to /app
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install any needed packages specified in requirements.txt
RUN pip install poetry
RUN poetry install

# Make port 8081 available to the world outside this container

EXPOSE 8000
EXPOSE 8081


# Define environment variable
ENV NAME World

# Run app.py when the container launches

# CMD ["/entrypoint.sh"]
# CMD ["python", "server.py"]
CMD ["poetry", "run", "python", "server.py"]
