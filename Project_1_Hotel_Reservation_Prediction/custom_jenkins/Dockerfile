

# -------------------------------------------------------------
# Use the official Jenkins LTS image as the base for CI/CD tasks
FROM jenkins/jenkins:lts

# -------------------------------------------------------------
# Switch to root user to install system-level dependencies
USER root

# -------------------------------------------------------------
# Install Docker using the modern keyring method (no apt-key)
RUN apt-get update -y && \
    apt-get install -y ca-certificates curl gnupg lsb-release && \
    install -m 0755 -d /etc/apt/keyrings && \
    curl -fsSL https://download.docker.com/linux/debian/gpg | gpg --dearmor -o /etc/apt/keyrings/docker.gpg && \
    chmod a+r /etc/apt/keyrings/docker.gpg && \
    echo \
      "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.gpg] https://download.docker.com/linux/debian \
      $(lsb_release -cs) stable" | tee /etc/apt/sources.list.d/docker.list > /dev/null && \
    apt-get update -y && \
    apt-get install -y docker-ce docker-ce-cli containerd.io && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

    
# -------------------------------------------------------------
# Add Jenkins user to the Docker group for Docker command access:
# - Ensures the 'docker' group exists
# - Adds Jenkins user to the group
RUN groupadd -f docker && \
    usermod -aG docker jenkins

# -------------------------------------------------------------
# Prepare Docker-in-Docker (DinD) environment:
# - Creates Docker data directory
# - Declares it as a volume for persistent storage
RUN mkdir -p /var/lib/docker
VOLUME /var/lib/docker

# -------------------------------------------------------------
# Switch back to Jenkins user for security best practices
USER jenkins