FROM python:3.11-slim

# Install dependencies
RUN apt-get update && apt-get install -y net-tools && rm -rf /var/lib/apt/lists/*

# Set the working directory
WORKDIR /app

# Copy application files
COPY . .

# Install Python dependencies
RUN pip install --no-cache-dir flask

# Expose port
EXPOSE 5000

# Run the application
CMD ["python", "network-info.py"]
