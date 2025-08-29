# Spark I/O Performance Research Project

A simplified environment for benchmarking Apache Spark I/O performance.

## 🚀 Quick Start

### Prerequisites

- Docker and Docker Compose
- 8GB+ RAM available for the cluster

### 1. Clone the Repository

```bash
git clone https://github.com/hoaihuongbk/spark-io-experience.git
cd spark-io-experience
chmod +x start_research_environment.sh
```

### 2. Start the Environment

```bash
make start
```
This command will start a multi-node Spark cluster, generate the TPC-DS dataset, ingest it into Parquet format, and set up optimized tables (partitioned and bucketed).

## 📊 Running Benchmarks

Run comprehensive I/O performance tests using `make benchmark`:

```bash
make benchmark
```

This command will execute a series of I/O and optimization benchmarks.

## 📈 Benchmark Results and Insights

- [Spark Join Optimization Benchmarks](benchmark_join_results.md)
- [Spark Partitioning Optimization Benchmarks](benchmark_partitioning_results.md)

## 🧹 Clean Up

To remove all generated data and log files:

```bash
make clean
```