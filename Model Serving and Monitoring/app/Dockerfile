FROM python:3.9-slim

WORKDIR /app

# Install dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    git \
    rsync \
    && rm -rf /var/lib/apt/lists/*

# Create a symlink for models if it's expected at /app/models
# The volume mount will be to /models, this symlink makes it accessible via /app/models
# Keep the symlink for general compatibility if other parts of app expect /app/models
RUN mkdir -p /app/models && ln -s /models /app/models

# Copy requirements first to leverage Docker cache
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Create directories needed by the application and entrypoint
RUN mkdir -p /app/logs /app/data /app/static/styles /app/metrics_data

# Copy source code
COPY ./app /app
COPY ./model_management /app/model_management
COPY ./monitoring /app/monitoring

# Copy the entrypoint script from the app directory (now the context is project root)
COPY ./app/entrypoint.sh /app/entrypoint.sh
RUN chmod +x /app/entrypoint.sh

# Set Python path to include parent directory and root
ENV PYTHONPATH=/app:/

# Set environment variable for style directory (used by entrypoint.sh)
ENV STYLES_DIR=/app/data/styles
ENV MODEL_PATH /models/model.pt

# Expose port
EXPOSE 8000

# Use the entrypoint script
ENTRYPOINT ["/app/entrypoint.sh"]

# Start FastAPI server (this will be passed as arguments to entrypoint.sh)
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"] 