# Use the official PostgreSQL image from Docker Hub
FROM postgres:15

# Set environment variables for the PostgreSQL database
ENV POSTGRES_USER=your_username
ENV POSTGRES_PASSWORD=your_password
ENV POSTGRES_DB=your_database_name
ENV DB_HOST=localhost
ENV DB_PORT=5432

# Install Netcat (nc) for waiting on DB readiness
RUN apt-get update && apt-get install -y --no-install-recommends netcat && apt-get clean

# Copy the custom entrypoint script into the container
COPY entrypoint.sh /usr/local/bin/entrypoint.sh

# Make the entrypoint script executable
RUN chmod +x /usr/local/bin/entrypoint.sh

# Set the custom entrypoint to use the script
ENTRYPOINT ["/usr/local/bin/entrypoint.sh"]

# Use the default command to start PostgreSQL
CMD ["postgres"]
