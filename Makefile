# Simple Spark I/O Research Makefile

.PHONY: help start stop benchmark clean status

help:
	@echo "🚀 Spark I/O Research - Simple Commands"
	@echo "======================================="
	@echo "  start     - Start Spark cluster"
	@echo "  stop      - Stop cluster"
	@echo "  benchmark - Run all I/O and optimization benchmarks"
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
benchmark:
	@echo "📊 Running all I/O and optimization benchmarks..."
	@docker-compose exec spark-master spark-submit \
		--master spark://spark-master:7077 \
		/opt/spark/scripts/benchmark.py

# Clean data and logs
clean:
	@echo "🧹 Cleaning data and logs..."
	@rm -rf data/* logs/*

# Show status
status:
	@echo "📊 Cluster status:"
	@docker-compose ps
