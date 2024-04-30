# Use the official Python base image
FROM python:3.9-slim

# Set the working directory in the container
WORKDIR /app

# Install Python dependencies
RUN pip install pandas numpy

# Copy the Python script into the container
COPY DescriptiveStats.py /app/

# Make sure the data directories exist
RUN mkdir /app/so_data
RUN mkdir /app/outcsv

# Copy the CSV files into the container within the so_data directory
# This command assumes that you have a directory `so_data` next to the Dockerfile
COPY so_data/*.csv /app/so_data/

# Set the environment variable to indicate the script is running inside Docker
ENV RUNNING_IN_DOCKER=true

# Set the entrypoint to use the script, the CMD will provide the model and number of threads
ENTRYPOINT ["python", "./DescriptiveStats.py"]
CMD ["1", "4", "10"]  # Default values: model 1, 4 threads, 10 iterations
