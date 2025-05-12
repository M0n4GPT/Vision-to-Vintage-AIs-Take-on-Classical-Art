FROM python:3.11-slim

WORKDIR /app

# Use modern ENV format to avoid warnings
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

COPY app.py /app/

RUN pip install --no-cache-dir dash pandas pillow

CMD ["python", "app.py"]
