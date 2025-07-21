# BombSquad Server Docker Setup

This Docker setup provides a lightweight, production-ready BombSquad server using Debian slim for optimal binary compatibility.

## Quick Start

1. **Copy the Docker configuration:**
   ```bash
   cp config.docker.toml config.toml
   ```

2. **Build and run the server:**
   ```bash
   docker-compose up -d
   ```

3. **Check server status:**
   ```bash
   docker-compose logs -f
   ```

## Configuration

### Environment Variables

You can customize the server using environment variables in `.env` file:

```bash
# Server settings
PARTY_NAME=My BombSquad Server
PARTY_IS_PUBLIC=false
AUTHENTICATE_CLIENTS=true
MAX_PARTY_SIZE=8
SESSION_TYPE=ffa
```

### Config File

For advanced configuration, edit `config.toml` directly. See the [CLAUDE.md](CLAUDE.md) file for configuration details.

## Management Commands

```bash
# Start the server
docker-compose up -d

# Stop the server
docker-compose down

# View logs
docker-compose logs -f

# Restart the server
docker-compose restart

# Update the server
docker-compose down
docker-compose build --no-cache
docker-compose up -d

# Access server shell (for debugging)
docker-compose exec bombsquad-server sh
```

## Network Requirements

- **UDP Port 43210**: Must be accessible from the internet for public servers
- **Firewall**: Ensure port 43210/udp is open in your firewall

## Troubleshooting

### Binary Compatibility
The Docker image uses Debian slim base for full glibc compatibility with the precompiled BombSquad binary. This ensures proper function symbol resolution and stable operation.

### Performance Issues
- Monitor resource usage: `docker stats bombsquad-server`
- Adjust resource limits in `docker-compose.yml`
- Check logs for errors: `docker-compose logs`

### Data Persistence
Server data is stored in named Docker volumes:
- `bombsquad-data`: Server state and cache
- `bombsquad-logs`: Server logs

To backup data:
```bash
docker run --rm -v bombsquad-data:/data -v $(pwd):/backup alpine tar czf /backup/bombsquad-backup.tar.gz /data
```

## Image Size
The final image size is approximately 80-120MB using Debian slim base, optimized for binary compatibility and deployment efficiency.