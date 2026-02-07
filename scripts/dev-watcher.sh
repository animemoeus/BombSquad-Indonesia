#!/bin/bash
# Development file watcher for BombSquad server
# Monitors mods/ directory and auto-restarts server on changes

set -e

echo "========================================="
echo "BombSquad Development Mode"
echo "========================================="
echo "Watching for file changes in:"
echo "  - /app/data/mods/"
echo "  - /app/config.toml"
echo ""
echo "Press Ctrl+C to stop"
echo "========================================="

# Install inotify-tools if not present
if ! command -v inotifywait &> /dev/null; then
    echo "Installing inotify-tools for file watching..."
    apt-get update -qq && apt-get install -y -qq inotify-tools
fi

# Function to start the server
start_server() {
    echo ""
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] Starting BombSquad server..."
    /app/bombsquad_server &
    SERVER_PID=$!
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] Server started with PID: $SERVER_PID"
}

# Function to stop the server
stop_server() {
    if [ ! -z "$SERVER_PID" ]; then
        echo ""
        echo "[$(date '+%Y-%m-%d %H:%M:%S')] Stopping server (PID: $SERVER_PID)..."
        kill -TERM $SERVER_PID 2>/dev/null || true
        wait $SERVER_PID 2>/dev/null || true
        echo "[$(date '+%Y-%m-%d %H:%M:%S')] Server stopped"
    fi
}

# Function to restart the server
restart_server() {
    local file=$1
    echo ""
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] File changed: $file"
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] Restarting server..."
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    stop_server
    sleep 1
    start_server
}

# Trap SIGTERM and SIGINT to gracefully shutdown
trap 'stop_server; exit 0' SIGTERM SIGINT

# Start the server initially
start_server

# Watch for file changes
echo ""
echo "[$(date '+%Y-%m-%d %H:%M:%S')] File watcher started. Waiting for changes..."

# Use inotifywait to monitor for changes
# -m: monitor continuously
# -r: recursive
# -e: events to watch for
inotifywait -m -r \
    -e modify,create,delete,move \
    --exclude '\.pyc$|__pycache__|\.git|\.swp$|\.tmp$' \
    /app/data/mods/ /app/config.toml 2>/dev/null | \
while read -r directory events filename; do
    # Debounce: ignore rapid successive changes
    if [ ! -z "$filename" ]; then
        # Only restart for .py files in mods or config.toml
        if [[ "$filename" =~ \.py$ ]] || [[ "$filename" == "config.toml" ]]; then
            restart_server "${directory}${filename}"
            # Wait a bit to avoid multiple rapid restarts
            sleep 2
        fi
    fi
done

# Keep the script running
wait $SERVER_PID
