# Use an official lightweight Python runtime
FROM python:3.11-slim

# Prevent Python from writing .pyc files and enable unbuffered logging
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Set workspace directory
WORKDIR /app

# Install system-level build tools
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    curl \
    && rm -rf /var/lib/apt-get/lists/*

# Copy dependency definition and install Python packages
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

# Copy application source code and PDF document
COPY . /app/

# Expose default Streamlit port
EXPOSE 8502

# Streamlit healthcheck
HEALTHCHECK CMD curl --fail http://localhost:8502/_stcore/health || exit 1

# Start Streamlit application
CMD ["streamlit", "run", "app.py", "--server.port=8502", "--server.address=0.0.0.0"]