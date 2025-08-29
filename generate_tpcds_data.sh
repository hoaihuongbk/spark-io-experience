#!/bin/bash

set -e

echo "🏗️ Building TPC-DS data generator image..."
docker build -t tpcds-generator -f tpcds.Dockerfile .

echo "📊 Generating TPC-DS data (Scale 1)..."
docker run --rm -v "$(pwd)/data:/data" tpcds-generator dsdgen -SCALE 1 -DIR /data

# Ingest TPC-DS data to Parquet and setup optimized tables
echo "⚙️ Ingesting TPC-DS data and setting up optimized tables..."
docker-compose exec spark-master spark-submit --master spark://spark-master:7077 /opt/spark/scripts/ingest_tpcds_data.py
docker-compose exec spark-master spark-submit --master spark://spark-master:7077 /opt/spark/scripts/setup_optimized_tables.py