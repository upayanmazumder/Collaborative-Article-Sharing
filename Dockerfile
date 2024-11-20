# Use the official Python image
FROM python:3.11

# Create and change to the app directory
WORKDIR /app
COPY api/requirements.txt ./api/

# Install dependencies for the api folder
WORKDIR /app/api
RUN pip install --no-cache-dir -r requirements.txt

# Copy the local code to the container image
WORKDIR /app
COPY . .

# Expose port 3000
EXPOSE 3000

# Run the web service on container startup
CMD ["gunicorn", "-c", "api/gunicorn_config.py", "api.main:app"]