FROM python:3.10-bookworm

# Install Piper TTS engine
RUN pip install piper-tts

# Create necessary directories with appropriate permissions
RUN mkdir -p /voice && mkdir -p /output && chmod -R 777 /output

# Copy voice models into the container
COPY voices/ /voice/

# Set the working directory
WORKDIR /app

# Copy the FastAPI app code into the container
COPY app/ .

# Install Python dependencies
RUN pip3 install -U -r requirements.txt

# Set environment variable for server port
ENV SERVER_PORT=8080

# Healthcheck to ensure the server is responsive
HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \
  CMD curl --fail http://localhost:${SERVER_PORT}/api/healthcheck || exit 1

# Command to run the server
CMD ["uvicorn", "piper_tts_server:app", "--host", "0.0.0.0", "--port", "8080"]
