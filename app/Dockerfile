# Setup the container with python 3.10.12
FROM python:3.10.12

# Copy necessary everything to the current directory in the container
COPY . /app

# Change working directory
WORKDIR /app

# Install the dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Expose port 8000
EXPOSE 8000

# Set command to run
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]