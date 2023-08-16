# Use the official Python image as a base image
FROM python:3.11-slim

# Set the working directory in the container
WORKDIR /app

# Install pipenv
RUN pip install pipenv

# Copy the Pipfile and Pipfile.lock into the container
COPY Pipfile Pipfile.lock ./

# Install dependencies using pipenv
RUN pipenv install --deploy --ignore-pipfile

# Copy the entire SiltServer directory into the container
COPY SiltServer/ SiltServer/

# Expose the port that FastAPI will run on
EXPOSE ${SERVER_ADDR_PORT}

# Run the FastAPI application
CMD ["pipenv", "run", "python", "SiltServer/main.py"]
