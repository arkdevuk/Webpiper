# FROM python:3.10-bookworm
# We need to use a CUDA container for GPU support
FROM nvidia/cuda:12.6.3-base-ubuntu20.04
# Then install Python and other dependencies like pip, git, uvicorn
# Install Python and other dependencies
RUN apt-get --allow-releaseinfo-change update
RUN sed -i 's|http://archive.ubuntu.com/ubuntu/|http://fr.archive.ubuntu.com/ubuntu/|g' /etc/apt/sources.list

RUN apt-get update && apt-get install -y --fix-missing \
    git \
    curl \
    build-essential \
    libffi-dev \
    libssl-dev

ENV DEBIAN_FRONTEND=noninteractive
RUN apt-get install -y software-properties-common
RUN add-apt-repository ppa:deadsnakes/ppa
RUN apt-get update && apt-get install -y python3.11 python3.11-venv python3.11-distutils

# Symlink for python and pip
RUN ln -sf /usr/bin/python3.11 /usr/bin/python && \
    ln -sf /usr/bin/python3.11 /usr/bin/python3

# Install pip for Python 3.11
RUN curl -sS https://bootstrap.pypa.io/get-pip.py -o get-pip.py && \
    python3.11 get-pip.py && \
    rm get-pip.py \
    && ln -sf /usr/local/bin/pip3.11 /usr/local/bin/pip \
    && ln -sf /usr/local/bin/pip3.11 /usr/local/bin/pip3
RUN python -m pip install --upgrade pip

RUN which python && which python3 && python --version && python3 --version

# Create a non-root user
RUN useradd -m -s /bin/bash appuser

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

# venv
RUN python3 -m venv /opt/venv \
 && /opt/venv/bin/pip install --no-cache-dir --upgrade pip \
 && /opt/venv/bin/pip install --no-cache-dir -r requirements.txt
ENV PATH="/opt/venv/bin:$PATH"


# Install Python dependencies
RUN python3 -m pip install --no-cache-dir --upgrade -r requirements.txt

# Set environment variable for server port
ENV SERVER_PORT=8080

# Healthcheck to ensure the server is responsive
#HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \
#  CMD curl --fail http://localhost:${SERVER_PORT}/api/healthcheck || exit 1

# Switch to non-root user
USER appuser

# Command to run the server
CMD ["uvicorn", "piper_tts_server:app", "--host", "0.0.0.0", "--port", "8080"]
# to test in cli you can run:
