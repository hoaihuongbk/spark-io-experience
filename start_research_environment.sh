#!/bin/bash

# Spark I/O Research Environment Startup Script
# This script sets up and starts the complete research environment

set -e

echo "🚀 Starting Spark I/O Research Environment..."
echo "=============================================="

# Check if Docker is running
if ! docker info > /dev/null 2>&1; then
    echo "❌ Docker is not running. Please start Docker and try again."
    exit 1
fi

# Check if Docker Compose is available
if ! command -v docker-compose &> /dev/null; then
    echo "❌ Docker Compose is not installed. Please install it and try again."
    exit 1
fi



# Create necessary directories if they don't exist
echo "📁 Creating necessary directories..."
mkdir -p data logs configs notebooks scripts research

# Set proper permissions
echo "🔐 Setting proper permissions..."
chmod 755 scripts/*.py
chmod 644 configs/*.conf



# Start the Spark cluster
echo "🐳 Starting Spark cluster with Docker Compose..."
docker-compose up -d

# Wait for services to be ready
echo "⏳ Waiting for services to be ready..."
sleep 30

# Check service status
echo "🔍 Checking service status..."
docker-compose ps

# Get Jupyter access token
echo "🔑 Getting Jupyter access information..."
JUPYTER_CONTAINER=$(docker-compose ps -q jupyter)
if [ ! -z "$JUPYTER_CONTAINER" ]; then
    echo "📊 Jupyter Lab is starting up..."
    echo "   Access URL: http://localhost:8888"
    echo "   Token authentication is enabled for security"
    echo ""
    echo "   To get the access token, run:"
    echo "   docker-compose logs jupyter | grep 'token='"
    echo ""
    echo "   Or check the logs:"
    echo "   docker-compose logs jupyter"
fi

# Show Spark UI information
echo "📈 Spark UI Information:"
echo "   Master UI: http://localhost:8080"
echo "   Master URL: spark://localhost:7077"

echo ""
echo "✅ Cluster starting! Wait a few minutes, then:"
echo "   make benchmark # Run benchmarks"
