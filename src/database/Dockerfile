FROM postgres:15

# Install Netcat (nc) for waiting on DB readiness
RUN apt-get update && \
    apt-get install -y --no-install-recommends && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Copy the custom entrypoint script into the container
COPY entrypoint.sh /usr/local/bin/entrypoint.sh

# Make the entrypoint script executable
RUN chmod +x /usr/local/bin/entrypoint.sh

# Set the custom entryp÷oint to use the script
# ENTRYPOINT ["/usr/local/bin/entrypoint.sh"]

# Use the default command to start PostgreSQL
# CMD ["postgres"]