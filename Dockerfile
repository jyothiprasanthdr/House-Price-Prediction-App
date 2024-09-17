FROM python:3.8

COPY . /app
# Set the working directory
WORKDIR /app

# Upgrade pip and install dependencies
RUN pip install --no-cache-dir  -r requirements.txt


# Set the default port

EXPOSE 10000

# Command to run the application
CMD gunicorn --workers=4 --timeout 120 --bind 0.0.0.0:10000 app:app
