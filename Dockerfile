# Use Python base image
FROM python:3.9-slim

# Set working directory
WORKDIR /app/ApicScripts

# Copy the ApicScripts folder to the container
COPY ApicScripts /app/ApicScripts

# Install Python dependencies
RUN pip install -r requirements.txt

# Download and set up the APIC CLI into the same directory as the scripts
ARG ARTIFACTORY_URL
ARG ARTIFACTORY_USER
ARG ARTIFACTORY_PASSWORD

RUN if [ -n "$ARTIFACTORY_URL" ] && [ -n "$ARTIFACTORY_USER" ] && [ -n "$ARTIFACTORY_PASSWORD" ]; then \
    echo "Downloading APIC CLI..."; \
    curl -u $ARTIFACTORY_USER:$ARTIFACTORY_PASSWORD -O $ARTIFACTORY_URL; \
    tar -xzf apic-cli.tar.gz; \
    chmod +x apic-cli; \
    mv apic-cli /app/ApicScripts/apic-cli; \
    rm apic-cli.tar.gz; \
    else \
    echo "Missing Artifactory credentials or URL. Skipping APIC CLI installation."; \
    fi

# Grant execute permissions to shell scripts
RUN chmod +x *.sh

# Set the default entry point to CallAllFunction.py
CMD ["python", "CallAllFunction.py"]
