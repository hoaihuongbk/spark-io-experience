# Simple Spark I/O Research Makefile

.PHONY: help start stop benchmark clean status generate-dataset benchmark-join benchmark-partitioning

help:
	@echo "🚀 Spark I/O Research - Simple Commands"
	@echo "======================================="
	@echo "  start     - Start Spark cluster"
	@echo "  stop      - Stop cluster"
	@echo "  benchmark - Run all I/O and optimization benchmarks (join and partitioning)"
	@echo "  benchmark-join - Run only join benchmarks"
	@echo "  benchmark-partitioning - Run only partitioning benchmarks"
	@echo "  generate-dataset - Generate TPC-DS data"
	@echo "  status    - Show cluster status"
	@echo "  clean     - Clean data and logs"
	@echo "  help      - Show this help"

# Start cluster
start:
	@echo "🚀 Starting Spark cluster..."
	@./start_research_environment.sh

# Stop cluster
stop:
	@echo "🛑 Stopping cluster..."
	@docker-compose down

# Run all I/O and optimization benchmarks
benchmark: benchmark-join benchmark-partitioning

# Run only join benchmarks
benchmark-join:
	@echo "📊 Running Join Benchmarks..."
	@docker-compose exec spark-master spark-submit \
		--master spark://spark-master:7077 \
		/opt/spark/scripts/benchmark_join.py

# Run only partitioning benchmarks
benchmark-partitioning:
	@echo "📊 Running Partitioning Benchmarks..."
	@docker-compose exec spark-master spark-submit \
		--master spark://spark-master:7077 \
		/opt/spark/scripts/benchmark_partitioning.py

# Generate TPC-DS data
generate-dataset:
	@echo "📦 Generating TPC-DS dataset..."
	@./generate_tpcds_data.sh

# Clean data and logs
clean:
	@echo "🧹 Cleaning data and logs..."
	@rm -rf data/* logs/*

# Show status
status:
	@echo "📊 Cluster status:"
	@docker-compose ps
