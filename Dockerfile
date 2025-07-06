# Dockerfile for Ubuntu Container with AI Agent
FROM ubuntu:22.04

# Set environment variables
ENV DEBIAN_FRONTEND=noninteractive
ENV PYTHONUNBUFFERED=1
ENV AGENT_HOME=/opt/agent

# Install system dependencies
RUN apt-get update && apt-get install -y \
    python3 \
    python3-pip \
    python3-venv \
    curl \
    wget \
    git \
    vim \
    nano \
    htop \
    tree \
    jq \
    unzip \
    build-essential \
    sudo \
    && rm -rf /var/lib/apt/lists/*

# Create agent directory
RUN mkdir -p $AGENT_HOME

# Copy agent files and requirements
COPY agent/ $AGENT_HOME/

# Convert CRLF to LF
RUN apt-get update && apt-get install -y dos2unix \
    && dos2unix $AGENT_HOME/agent.py \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt $AGENT_HOME/


WORKDIR $AGENT_HOME

# Install Python deps including Click & Gemini SDK
RUN pip3 install -r requirements.txt click google-generativeai

# Make agent.py executable & provide CLI symlink
RUN chmod +x agent.py \
    && ln -s $AGENT_HOME/agent.py /usr/local/bin/agent

# Create a non-root user 'agent' with sudo privileges
RUN useradd -m -s /bin/bash agent && \
    echo "agent ALL=(ALL) NOPASSWD:ALL" >> /etc/sudoers

USER agent

# Ensure ~/agent visibility in PATH
RUN echo 'export PATH=$PATH:/usr/local/bin' >> ~/.bashrc

EXPOSE 8080


