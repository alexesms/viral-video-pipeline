FROM python:3.11-slim

# Install only ffmpeg for video processing
RUN apt-get update && apt-get install -y ffmpeg && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Copy code
COPY . .

# Install Python deps
RUN pip install --no-cache-dir requests edge-tts yt-dlp

# Keep running
CMD ["tail", "-f", "/dev/null"]
