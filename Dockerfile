FROM python:3.8

COPY . /app
# Set the working directory
WORKDIR /app

# Upgrade pip and install dependencies
RUN pip install --no-cache-dir  -r requirements.txt


# Set the default port

EXPOSE 7596

# Command to run the application
CMD gunicorn --timeout 300 --workers 2 --max-requests 1000 --max-requests-jitter 50 --bind 0.0.0.0:7596 app:app

RUN apt-get update && apt-get install -y htop

# Add a healthcheck
HEALTHCHECK --interval=30s --timeout=30s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:7596/ || exit 1