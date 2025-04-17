FROM python:3.10-bookworm

# Create a non-root user
RUN useradd -m -s /bin/bash appuser

# Install Piper TTS engine
RUN pip install piper-tts

# Create necessary directories with appropriate permissions
RUN mkdir -p /voice && mkdir -p /output && chmod -R 777 /output

# Create necessary directories and adjust permissions
RUN mkdir -p /voice /output /app && \
    chmod -R 755 /voice /output /app && \
    chown -R appuser:appuser /voice /output /app

# Copy voice models into the container
COPY voices/ /voice/

# create app directory and set permissions
RUN chown appuser:appuser /app

# Set the working directory
WORKDIR /app

# Copy the FastAPI app code into the container
COPY app/ .

# Switch to non-root user
USER appuser

# Install Python dependencies
RUN pip3 install -U -r requirements.txt

# Set environment variable for server port
ENV SERVER_PORT=8080

# Healthcheck to ensure the server is responsive
HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \
  CMD curl --fail http://localhost:${SERVER_PORT}/api/healthcheck || exit 1

# Command to run the server
CMD ["uvicorn", "piper_tts_server:app", "--host", "0.0.0.0", "--port", "8080"]
