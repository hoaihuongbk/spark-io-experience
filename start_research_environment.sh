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
mkdir -p data logs

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


# Build TPC-DS data generator image
echo "🏗️ Building TPC-DS data generator image..."
docker build -t tpcds-generator -f tpcds.Dockerfile .

# Generate TPC-DS data
echo "📊 Generating TPC-DS data (Scale 1)..."
docker run --rm -v "$(pwd)/data:/data" tpcds-generator dsdgen -SCALE 1 -DIR /data

# Run data ingestion and table setup scripts
echo "⚙️ Ingesting TPC-DS data and setting up optimized tables..."
docker-compose exec spark-master spark-submit --master spark://spark-master:7077 /opt/spark/scripts/ingest_tpcds_data.py
docker-compose exec spark-master spark-submit --master spark://spark-master:7077 /opt/spark/scripts/setup_optimized_tables.py

echo ""
echo "✅ Cluster starting! Wait a few minutes, then:"
echo "   make benchmark # Run benchmarks"
