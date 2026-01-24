FROM python:3.12-slim

# Install git
RUN apt-get update && \
    apt-get install -y \
      git \
    && apt-get clean && rm -rf /var/lib/apt/lists/*

# Directory for local bin
ENV PATH="/root/.local/bin:${PATH}"
RUN mkdir -p /root/.local/bin

# Set working directory
WORKDIR /app
