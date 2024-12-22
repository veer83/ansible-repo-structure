# Use Python base image
FROM python:3.9-slim

# Set working directory
WORKDIR /app

# Copy project files to the container
COPY . /app

# Install Python dependencies
RUN pip install -r requirements.txt

# Define build arguments for APIC CLI
ARG ARTIFACTORY_URL
ARG ARTIFACTORY_USER
ARG ARTIFACTORY_PASSWORD

# Download APIC CLI and set it up
RUN if [ -n "$ARTIFACTORY_URL" ] && [ -n "$ARTIFACTORY_USER" ] && [ -n "$ARTIFACTORY_PASSWORD" ]; then \
    echo "Downloading APIC CLI from Artifactory..."; \
    curl -u $ARTIFACTORY_USER:$ARTIFACTORY_PASSWORD -O $ARTIFACTORY_URL/apic; \
    chmod +x apic; \
    mv apic-cli /usr/local/bin/apic; \
    else \
    echo "Artifactory credentials or URL missing. Skipping APIC CLI setup."; \
    fi

# Grant execution permissions to shell scripts
RUN chmod +x *.sh

# Default command to execute the main script
CMD ["python", "CallAllFunction.py"]
