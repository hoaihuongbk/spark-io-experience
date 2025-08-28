# Simple Spark I/O Research Makefile

.PHONY: help start stop benchmark test status clean

help:
	@echo "🚀 Spark I/O Research - Simple Commands"
	@echo "======================================="
	@echo "  start     - Start Spark cluster"
	@echo "  stop      - Stop cluster"
	@echo "  benchmark - Run benchmarks in cluster"
	@echo "  test      - Test cluster"
	@echo "  status    - Show status"
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



# Run benchmarks in cluster
benchmark:
	@echo "📊 Running shuffle compression disabled benchmark..."
	@docker-compose exec spark-master spark-submit \
		--master spark://spark-master:7077 \
		--conf spark.shuffle.compress=false \
		--conf spark.shuffle.spill.compress=false \
		/opt/spark/scripts/unified_benchmark.py shuffle_disabled

	@echo "📊 Running shuffle compression enabled benchmark..."
	@docker-compose exec spark-master spark-submit \
		--master spark://spark-master:7077 \
		--conf spark.shuffle.compress=true \
		--conf spark.shuffle.spill.compress=true \
		/opt/spark/scripts/unified_benchmark.py shuffle_enabled

	@echo "📊 Running I/O Snappy benchmark..."
	@docker-compose exec spark-master spark-submit \
		--master spark://spark-master:7077 \
		--conf spark.sql.parquet.compression.codec=snappy \
		/opt/spark/scripts/unified_benchmark.py io_snappy snappy

	@echo "📊 Running I/O Gzip benchmark..."
	@docker-compose exec spark-master spark-submit \
		--master spark://spark-master:7077 \
		--conf spark.sql.parquet.compression.codec=gzip \
		/opt/spark/scripts/unified_benchmark.py io_gzip gzip

	@echo "📊 Running I/O Zstd benchmark..."
	@docker-compose exec spark-master spark-submit \
		--master spark://spark-master:7077 \
		--conf spark.sql.parquet.compression.codec=zstd \
		/opt/spark/scripts/unified_benchmark.py io_zstd zstd



# Test cluster
test:
	@echo "🧪 Testing cluster..."
	

# Clean data and logs
clean:
	@echo "🧹 Cleaning data and logs..."
	@rm -rf data/* logs/*

# Show status
status:
	@echo "📊 Cluster status:"
	@docker-compose ps

