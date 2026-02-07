# Development Guide - BombSquad Server

Guide untuk development lokal dengan auto-reload ketika ada perubahan code.

## 🚀 Quick Start

### Start Development Server

```bash
# Build dan start dengan auto-reload
docker compose -f docker-compose.yml -f docker-compose.dev.yml up --build

# Atau gunakan alias
docker compose -f docker-compose.yml -f docker-compose.dev.yml up
```

### Stop Development Server

```bash
# Stop server
docker compose -f docker-compose.yml -f docker-compose.dev.yml down

# Atau Ctrl+C di terminal
```

## 📁 File Structure

```
BombSquad-Indonesia/
├── mods/                           # Custom plugins (AUTO-RELOAD!)
│   ├── server_customizations.py    # Main plugin
│   └── README.md
├── scripts/                        # Development scripts
│   └── dev-watcher.sh             # File watcher untuk auto-reload
├── docker-compose.yml              # Production config
├── docker-compose.dev.yml          # Development overrides
├── Dockerfile                      # Multi-stage: base + development
└── DEV.md                         # File ini
```

## 🔄 Auto-Reload Behavior

File watcher akan **otomatis restart server** ketika detect perubahan di:

### ✅ Monitored Files:
- **`mods/**/*.py`** - Semua Python files di mods/
- **`config.toml`** - Server configuration

### ❌ Ignored Files:
- `*.pyc` - Compiled Python
- `__pycache__/` - Python cache
- `.git/` - Git directory
- `*.swp`, `*.tmp` - Temporary files

### Debounce:
- Watcher tunggu 2 detik setelah detect change sebelum restart
- Ini prevent multiple restarts untuk rapid successive changes

## 💻 Development Workflow

### 1. Start Development Server

```bash
docker compose -f docker-compose.yml -f docker-compose.dev.yml up
```

Output:
```
=========================================
BombSquad Development Mode
=========================================
Watching for file changes in:
  - /app/data/mods/
  - /app/config.toml

Press Ctrl+C to stop
=========================================

[2024-01-20 10:30:45] Starting BombSquad server...
[2024-01-20 10:30:45] Server started with PID: 123
[2024-01-20 10:30:45] File watcher started. Waiting for changes...
```

### 2. Edit Code

Edit file di `mods/server_customizations.py`:

```python
# Change shield brightness
SHIELD_BRIGHTNESS_MULTIPLIER = 1.5  # Changed from 1.2
```

Save file (Ctrl+S).

### 3. Auto-Reload Happens

Server akan restart otomatis:

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
[2024-01-20 10:31:20] File changed: /app/data/mods/server_customizations.py
[2024-01-20 10:31:20] Restarting server...
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

[2024-01-20 10:31:20] Stopping server (PID: 123)...
[2024-01-20 10:31:20] Server stopped
[2024-01-20 10:31:21] Starting BombSquad server...
[2024-01-20 10:31:21] Server started with PID: 456
```

### 4. Test Changes

Join server dan test perubahan:
- Shield sekarang lebih bright (1.5x instead of 1.2x)

## 🔧 Development Features

### Volume Mounts (Read-Write)

| Host Path | Container Path | Purpose |
|-----------|---------------|---------|
| `./mods/` | `/app/data/mods/` | Plugin development (RW) |
| `./config.docker.toml` | `/app/config.toml` | Server config (RW) |
| `bombsquad-data-dev` | `/app/data/` | Data persistence |
| `bombsquad-logs-dev` | `/app/logs/` | Logs |

### Environment Overrides

Development mode sets:
```yaml
PARTY_NAME: "[DEV] BombSquad Server"  # Prefix with [DEV]
PARTY_IS_PUBLIC: false                # Don't list publicly
AUTHENTICATE_CLIENTS: false           # Allow unauthenticated (faster testing)
DEV_MODE: 1                          # Enable dev mode
LOG_LEVEL: DEBUG                     # Verbose logging
```

### Development Tools Included

Container includes:
- **inotify-tools** - File watching
- **procps** - Process management (ps, pgrep, kill)
- **vim** - Text editor
- **less** - File viewer

### No Auto-Restart Policy

```yaml
restart: "no"
```

Di development mode, container TIDAK auto-restart kalau crash. Ini bagus untuk:
- Debug crashes lebih mudah
- Lihat error messages sebelum restart
- Prevent infinite restart loops

## 📝 Common Development Tasks

### Edit Plugin Code

```bash
# Edit dengan editor favorit
vim mods/server_customizations.py
code mods/server_customizations.py
nano mods/server_customizations.py

# Save file → Auto-reload!
```

### Edit Server Config

```bash
vim config.docker.toml

# Save → Auto-reload!
```

### View Logs

```bash
# Follow logs (tail -f)
docker compose -f docker-compose.yml -f docker-compose.dev.yml logs -f

# View specific service
docker compose -f docker-compose.yml -f docker-compose.dev.yml logs -f bombsquad-server

# View last 100 lines
docker compose -f docker-compose.yml -f docker-compose.dev.yml logs --tail=100
```

### Execute Commands in Container

```bash
# Open shell
docker compose -f docker-compose.yml -f docker-compose.dev.yml exec bombsquad-server bash

# View running processes
docker compose -f docker-compose.yml -f docker-compose.dev.yml exec bombsquad-server ps aux

# Check mods directory
docker compose -f docker-compose.yml -f docker-compose.dev.yml exec bombsquad-server ls -la /app/data/mods/
```

### Rebuild Image

```bash
# Rebuild development image
docker compose -f docker-compose.yml -f docker-compose.dev.yml build

# Force rebuild (no cache)
docker compose -f docker-compose.yml -f docker-compose.dev.yml build --no-cache
```

### Clean Up Development Data

```bash
# Remove development volumes
docker compose -f docker-compose.yml -f docker-compose.dev.yml down -v

# This will delete:
# - bombsquad-data-dev
# - bombsquad-logs-dev
```

## 🎯 Development vs Production

| Feature | Development | Production |
|---------|-------------|------------|
| **Auto-reload** | ✅ Yes | ❌ No |
| **Volumes** | Read-Write | Read-Only |
| **Party Name** | `[DEV]` prefix | Configurable |
| **Public Listing** | Disabled | Configurable |
| **Authentication** | Disabled | Enabled |
| **Restart Policy** | None | `unless-stopped` |
| **Log Level** | DEBUG | INFO |
| **Dev Tools** | Included | Not included |

## 🐛 Troubleshooting

### Auto-reload tidak work

**Check file watcher running:**
```bash
docker compose -f docker-compose.yml -f docker-compose.dev.yml exec bombsquad-server ps aux | grep inotify
```

**Check watcher logs:**
```bash
docker compose -f docker-compose.yml -f docker-compose.dev.yml logs | grep "File changed"
```

**Manual restart:**
```bash
docker compose -f docker-compose.yml -f docker-compose.dev.yml restart
```

### Server crash loop

**View crash logs:**
```bash
docker compose -f docker-compose.yml -f docker-compose.dev.yml logs --tail=50
```

**Check Python syntax:**
```bash
python3 -m py_compile mods/server_customizations.py
```

**Disable auto-reload:**
Edit `docker-compose.dev.yml`, change command to:
```yaml
command: ["./bombsquad_server"]
```

### File permissions error

```bash
# Fix ownership (di host)
sudo chown -R $USER:$USER mods/

# Or in container
docker compose -f docker-compose.yml -f docker-compose.dev.yml exec --user root bombsquad-server chown -R bombsquad:bombsquad /app/data/mods/
```

### Port already in use

```bash
# Check what's using port 43210
sudo lsof -i :43210

# Stop production server first
docker compose down

# Then start dev server
docker compose -f docker-compose.yml -f docker-compose.dev.yml up
```

## 🔥 Hot Tips

### Alias untuk Development

Tambah ke `~/.bashrc` atau `~/.zshrc`:

```bash
# BombSquad development aliases
alias bs-dev='docker compose -f docker-compose.yml -f docker-compose.dev.yml'
alias bs-dev-up='docker compose -f docker-compose.yml -f docker-compose.dev.yml up'
alias bs-dev-down='docker compose -f docker-compose.yml -f docker-compose.dev.yml down'
alias bs-dev-logs='docker compose -f docker-compose.yml -f docker-compose.dev.yml logs -f'
alias bs-dev-shell='docker compose -f docker-compose.yml -f docker-compose.dev.yml exec bombsquad-server bash'
```

Reload shell:
```bash
source ~/.bashrc
```

Usage:
```bash
bs-dev up        # Start dev server
bs-dev-logs      # View logs
bs-dev-shell     # Open shell
bs-dev down      # Stop server
```

### Watch Specific Plugin Loading

```bash
docker compose -f docker-compose.yml -f docker-compose.dev.yml logs -f | grep ServerCustomizations
```

### Quick Test Cycle

```bash
# Terminal 1: Run dev server
bs-dev-up

# Terminal 2: Watch logs
bs-dev-logs | grep -E "ServerCustomizations|File changed"

# Terminal 3: Edit code
vim mods/server_customizations.py
```

### Temporarily Disable Plugin

```bash
# Rename to disable
mv mods/server_customizations.py mods/server_customizations.py.disabled
# Server auto-reloads without plugin

# Re-enable
mv mods/server_customizations.py.disabled mods/server_customizations.py
# Server auto-reloads with plugin
```

## 📚 Next Steps

1. **Read Plugin Documentation**: `mods/README.md`
2. **Check Server Config**: `config.docker.toml`
3. **Review Base Code**: `dist/ba_data/python/`
4. **Join Development Server**: Port 43210

## 🤝 Contributing

When developing:
1. ✅ Keep changes in `mods/` directory
2. ✅ Test with development server
3. ✅ Document changes in code comments
4. ❌ Don't modify files in `dist/` (unless absolutely necessary)
5. ✅ Use git to track changes in `mods/`

Happy coding! 🎮
