# Use lightweight Python Debian slim image for glibc compatibility
FROM python:3.13-slim

# Install required system dependencies and create machine-id
RUN apt-get update && apt-get install -y --no-install-recommends \
    dbus \
    && rm -rf /var/lib/apt/lists/* \
    && dbus-uuidgen > /etc/machine-id

# Create non-root user for security
RUN useradd --create-home --shell /bin/bash bombsquad

# Set working directory
WORKDIR /app

# Copy the entire bombsquad server directory
COPY --chown=bombsquad:bombsquad . .

# Make executables (Debian supports the original shebang)
RUN chmod +x bombsquad_server dist/bombsquad_headless

# Create data directory for logs and cache
RUN mkdir -p data && chown bombsquad:bombsquad data

# Switch to non-root user
USER bombsquad

# Expose the default BombSquad port
EXPOSE 43210/udp

# Set environment variables
ENV PYTHONUNBUFFERED=1
ENV BA_ROOT=/app/data

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD pgrep -f bombsquad_headless || exit 1

# Run the server (original script handles Python flags)
CMD ["./bombsquad_server"]