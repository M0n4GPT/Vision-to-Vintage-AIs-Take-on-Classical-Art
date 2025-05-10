# Use official Python image
FROM python:3.11-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set working directory inside container
WORKDIR /app

# Copy only requirements first for caching
COPY app.py /app/

# Install required packages
RUN pip install --no-cache-dir dash pandas pillow

# Expose port
EXPOSE 8050

# Run the dashboard
CMD ["python", "app.py"]
