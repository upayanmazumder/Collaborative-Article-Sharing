# Use the official Python image
FROM python:3.11

# Create and change to the app directory
WORKDIR /app
COPY requirements.txt ./

# Install dependencies for the api folder
WORKDIR /app
RUN pip install --no-cache-dir -r requirements.txt

# Copy the local code to the container image
WORKDIR /app
COPY . .

# Expose port 4000
EXPOSE 4000

# Run the web service on container startup
CMD ["gunicorn", "-c", "gunicorn_config.py", "main:app"]