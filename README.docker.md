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

## Development Mode

For local development with auto-reload on code changes, use the development setup:

### Quick Start (Development)

```bash
# Using Makefile (recommended)
make dev

# Or using docker compose directly
docker compose -f docker-compose.yml -f docker-compose.dev.yml up
```

### Features

- **Auto-reload**: Server automatically restarts when files in `mods/` change
- **Live editing**: All code mounted as read-write volumes
- **Debug mode**: Verbose logging and development tools included
- **Isolated**: Separate volumes from production (`bombsquad-data-dev`)

### Development Commands (with Makefile)

```bash
make help          # Show all available commands
make dev           # Start development server
make dev-logs      # View logs
make dev-shell     # Open shell in container
make dev-down      # Stop development server
make plugin-check  # Check Python syntax
```

### File Watcher

Development mode uses `inotify` to watch for changes in:
- `mods/**/*.py` - All Python plugins
- `config.toml` - Server configuration

When a file changes, the server automatically restarts within 2 seconds.

### Development vs Production

| Feature | Development | Production |
|---------|-------------|------------|
| Auto-reload | ✅ Yes | ❌ No |
| Public listing | Disabled | Configurable |
| Auth required | Disabled | Enabled |
| Log level | DEBUG | INFO |
| Volumes | Read-Write | Read-Only |

### Documentation

See [DEV.md](DEV.md) for comprehensive development guide including:
- Detailed workflow
- Troubleshooting
- Hot tips and aliases
- Contributing guidelines