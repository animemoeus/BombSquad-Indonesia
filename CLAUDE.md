# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a BombSquad dedicated server setup - a multiplayer party game server. The project consists of:

- **bombsquad_server**: Python executable script that manages the game server
- **config.toml**: Server configuration file (copied from config_template.toml)
- **dist/**: Contains the complete BombSquad game distribution including:
  - Game data (maps, languages, fonts, meshes)
  - Python modules (babase, bascenev1, bauiv1, etc.)
  - Headless server binary

## Running the Server

**Primary command:**
```bash
./bombsquad_server
```

**Platform-specific notes:**
- Linux/Mac: `./bombsquad_server` 
- Windows: `launch_bombsquad_server.bat`
- Default UDP port: 43210 (configurable in config.toml)

## Configuration

Server configuration is managed through `config.toml`. Key settings include:
- `party_name`: Server name in public listing
- `party_is_public`: Whether to appear in global server list
- `authenticate_clients`: Enable client authentication via master server
- `admins`: Array of admin account IDs
- `port`: UDP port (default 43210)
- `max_party_size`: Maximum connected devices
- `session_type`: Game mode ("ffa", "teams", "coop")
- `playlist_code`: Custom playlist from game's playlist editor

## Architecture

**Server Manager (`bombsquad_server`):**
- Python 3.13+ script that manages server subprocess lifecycle
- Handles configuration loading from TOML
- Manages auto-restart, graceful shutdown, idle detection
- Uses `bacommon.servermanager` and `efro` modules from dist/

**Game Distribution (`dist/`):**
- Self-contained BombSquad installation
- Python modules organized by functionality:
  - `babase`: Core app framework and utilities
  - `bascenev1`: Game scene management, actors, sessions
  - `bascenev1lib`: Game implementations, maps, activities
  - `bauiv1`: UI framework
  - `efro`: Utility libraries for RPC, logging, data handling

**Game Data:**
- Maps: JSON definitions for game levels
- Languages: Localization files for international support
- Assets: Fonts, meshes, collision data

## Development Workflows

**Configuration changes:**
1. Edit `config.toml` 
2. Restart server: `./bombsquad_server`

**Server debugging:**
- Server logs to console output
- Use screen/tmux for remote access via SSH
- No telnet access (removed for security)

**Custom content:**
- Game code in `dist/ba_data/python/`
- Custom playlists via playlist_code or playlist_inline in config
- Map/game modifications require understanding bascenev1lib structure

## Network Setup

- Open UDP port 43210 (or custom port from config.toml)
- IPv4 address required for public server listing
- IPv6 optional but recommended
- LAN discovery only works on port 43210