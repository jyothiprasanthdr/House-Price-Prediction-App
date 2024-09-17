FROM python:3.8

COPY . /app
# Set the working directory
WORKDIR /app

# Upgrade pip and install dependencies
RUN pip install --no-cache-dir  -r requirements.txt


# Set the default port

EXPOSE 7596

# Command to run the application
CMD gunicorn --timeout 600 --workers 4 --bind 0.0.0.0:7596 app:app

