FROM python:3.10-slim

WORKDIR /app

# Copy the requirements and install them
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

# Copy the Flask app
COPY . .

# Expose the port Flask is running on
EXPOSE 5000

# Add health check (Flask default port is 5000)
HEALTHCHECK --interval=30s --timeout=10s --retries=3 CMD curl --fail http://localhost:5000/health || exit 1

# Start the Flask app
CMD ["python", "app.py"]
