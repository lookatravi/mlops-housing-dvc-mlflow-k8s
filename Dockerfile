# Use slim Python image (match MLflow compatibility)
FROM python:3.12-slim

# Python runtime settings
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# App directory
WORKDIR /opt/housing-ml-api

# Install OS dependencies
RUN apt-get update \
 && apt-get install -y --no-install-recommends gcc libc-dev \
 && rm -rf /var/lib/apt/lists/*

# Copy requirements first (better caching)
COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

# Copy application code + mlruns
COPY src ./src
COPY mlruns ./mlruns

# Environment variables (same as EC2 systemd)
ENV MLRUNS_DIR=/opt/housing-ml-api/mlruns
ENV MLFLOW_TRACKING_URI=file:/opt/housing-ml-api/mlruns
ENV MODEL_PATH=/opt/housing-ml-api/mlruns/292163823275666302/models/m-f4c983a17b8244799713aa308b8101aa/artifacts

# Expose API port
EXPOSE 6000

# Start with Gunicorn
CMD ["gunicorn", "--workers", "2", "--bind", "0.0.0.0:6000", "src.wsgi:app"]
