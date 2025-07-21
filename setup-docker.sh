#!/bin/bash
# BombSquad Server Docker Setup Script

set -e

echo "🏗️  Setting up BombSquad Server with Docker..."

# Check if Docker is installed
if ! command -v docker &> /dev/null; then
    echo "❌ Docker is not installed. Please install Docker first."
    exit 1
fi

# Check if Docker Compose is available
if ! docker compose version &> /dev/null; then
    echo "❌ Docker Compose is not available. Please install Docker Compose."
    exit 1
fi

# Create .env file if it doesn't exist
if [[ ! -f .env ]]; then
    echo "📝 Creating .env file from template..."
    cp .env.example .env
    echo "✅ Created .env file. You can edit it to customize your server settings."
fi

# Build and start the server
echo "🐳 Building Docker image..."
docker compose build

echo "🚀 Starting BombSquad server..."
docker compose up -d

echo "📊 Checking server status..."
sleep 5
docker compose ps

echo ""
echo "✅ BombSquad server setup complete!"
echo ""
echo "📝 Useful commands:"
echo "   View logs:    docker compose logs -f"
echo "   Stop server:  docker compose down"
echo "   Restart:      docker compose restart"
echo "   Update:       docker compose build --no-cache && docker compose up -d"
echo ""
echo "🌐 Server will be accessible on UDP port 43210"
echo "📁 Edit config.docker.toml to customize server settings"
echo "🔧 Edit .env to change basic server parameters"