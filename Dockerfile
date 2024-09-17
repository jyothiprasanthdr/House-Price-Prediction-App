FROM python:3.8

COPY . /app
# Set the working directory
WORKDIR /app

# Upgrade pip and install dependencies
RUN pip install --no-cache-dir  -r requirements.txt


# Set the default port

EXPOSE 8000

# Command to run the application
CMD gunicorn --workers=2 --timeout 300 --bind 127.0.0.1:8000 app:app
