# Use the official Python 3.12 runtime as base image
FROM python:3.12-slim

# Set environment variables to prevent Python from buffering stdout/stderr
ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1

# Set the working directory in the container
WORKDIR /app

# Copy requirements file first to leverage Docker cache
COPY requirements.txt .

# Install Python dependencies with diagnostic output
RUN echo "=== Installing Python dependencies ===" && \
    pip install --no-cache-dir -r requirements.txt && \
    echo "=== Dependencies installed successfully ===" && \
    pip list

# Install pytest for running unit tests
RUN pip install --no-cache-dir pytest pytest-cov

# Copy the main application files and dependencies
COPY culture_officer.py .
COPY config.py .
COPY format_culture_html.py .
COPY cultural_officer_system_prompt.py .

# Set environment variables from .env.docker file
ENV EMAIL_RECIPIENT=guez.ofer@gmail.com
ENV EMAIL_RECIPIENT_2=nachush2000@gmil.com
ENV EMAIL_SENDER=guez.ofer@gmail.com
ENV SENDGRID_API_KEY=your-sendgrid-api-key
ENV GOOGLE_PLACES_API_KEY=your-google-places-api-key
ENV SEARCH_RADIUS_MILES=50
ENV DEBUG=true

# Copy test files
COPY tests/ tests/

# Add diagnostic prints for file verification
RUN echo "=== Verifying copied files ===" && \
    ls -la /app && \
    echo "=== Test directory contents ===" && \
    find tests/ -name "*.py" | head -10

# Create directory for debug output (optional)
RUN mkdir -p /app/obs

# Run unit tests with diagnostic output
RUN echo "=== Running Unit Tests ===" && \
    python -m pytest tests/unittests/test_culture_officer_formatter.py -v --tb=short && \
    echo "=== Unit Tests Completed Successfully ==="

# Expose port 8080 (default for Google Cloud Functions)
EXPOSE 8080

# Add diagnostic print before starting the service
RUN echo "=== Container build completed successfully ===" && \
    echo "Python version: $(python --version)" && \
    echo "Working directory: $(pwd)" && \
    echo "Available files: $(ls -la)"

# Set the default command to run the functions framework
# This will serve the 'handler' function from culture_officer.py
CMD echo "=== Starting Functions Framework ===" && \
    functions-framework --target=handler --source=culture_officer.py --host=0.0.0.0 --port=8080