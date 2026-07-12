FROM python:3.11-slim

# Install system dependencies
RUN apt-get update && apt-get install -y \
    ffmpeg \
    git \
    curl \
    wget \
    cron \
    && rm -rf /var/lib/apt/lists/*

# Install Node.js
RUN curl -fsSL https://deb.nodesource.com/setup_20.x | bash - \
    && apt-get install -y nodejs \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Copy requirements first for caching
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Install CLI tools
RUN pip install --no-cache-dir \
    yt-dlp \
    edge-tts \
    moviepy

# Copy application code
COPY . .

# Create necessary directories
RUN mkdir -p /app/output /app/queue /app/posted /app/revenue

# Make scripts executable
RUN chmod +x *.sh 2>/dev/null || true

# Create cron job for daily runs at 8 AM UTC
RUN echo "0 8 * * * cd /app && python3 workflow_orchestrator.py --mode=daily >> /app/cron.log 2>&1" > /etc/cron.d/pipeline
RUN chmod 0644 /etc/cron.d/pipeline
RUN crontab /etc/cron.d/pipeline

# Keep container running and show logs
CMD cron && tail -f /app/cron.log /app/output/*.log 2>/dev/null || sleep infinity
