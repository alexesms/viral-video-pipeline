FROM python:3.11-slim

# Install ffmpeg and cron
RUN apt-get update && apt-get install -y \
    ffmpeg \
    cron \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Copy code
COPY . .

# Install Python deps
RUN pip install --no-cache-dir requests edge-tts yt-dlp

# Create cron job for daily runs at 8 AM UTC
RUN echo "0 8 * * * cd /app && python3 workflow_orchestrator.py --mode=daily >> /app/pipeline.log 2>&1" > /etc/cron.d/pipeline
RUN chmod 0644 /etc/cron.d/pipeline
RUN crontab /etc/cron.d/pipeline

# Create log file
RUN touch /app/pipeline.log

# Start cron and tail logs
CMD cron && tail -f /app/pipeline.log
