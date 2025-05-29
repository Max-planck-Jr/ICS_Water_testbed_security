# Use the official Ubuntu base image
FROM ubuntu:latest



# Avoid interactive prompts during package installation
ENV DEBIAN_FRONTEND=noninteractive

# Update package lists and install some common utilities
RUN apt-get update && apt-get install -y \
    curl \
    wget \
    vim \
    git \
    net-tools \
    iputils-ping \
    nano \
    && rm -rf /var/lib/apt/lists/*

# Set a working directory inside the container
WORKDIR /app


# Define the default command (change this if needed)
CMD ["/bin/bash"]
