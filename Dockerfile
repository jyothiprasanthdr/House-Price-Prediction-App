FROM python:3.7

# Set the working directory
WORKDIR /app

# Copy the requirements file first to leverage Docker cache
COPY requirements.txt .




# Upgrade pip and install dependencies
RUN pip install  -r requirements.txt

# Copy the rest of the application code
COPY . .

# Set the default port
ENV PORT=8000
EXPOSE $PORT

# Command to run the application
CMD gunicorn --workers=4 --bind 127.0.0.1:$PORT app:app
