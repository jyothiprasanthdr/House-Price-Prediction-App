FROM python:3.8

COPY . /app
# Set the working directory
WORKDIR /app

# Upgrade pip and install dependencies
RUN pip install  -r requirements.txt


# Set the default port

EXPOSE 5000

# Command to run the application
CMD gunicorn --workers=4 --bind 0.0.0.0:5000 app:app
