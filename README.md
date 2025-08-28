# Spark I/O Performance Research Project

A simplified environment for benchmarking Apache Spark I/O performance.

## 🚀 Quick Start

### Prerequisites

- Docker and Docker Compose
- 8GB+ RAM available for the cluster

### 1. Clone the Repository

```bash
git clone <repository-url>
cd spark_io_explore
chmod +x start_research_environment.sh
```

### 2. Start the Environment

```bash
./start_research_environment.sh
```

This will start a 3-node Spark cluster.

### 3. Access Spark UI

- **Spark Master UI**: http://localhost:8080
- **Spark Master URL**: `spark://localhost:7077`

## 📊 Running Benchmarks

Run comprehensive I/O performance tests using `make benchmark`:

```bash
make benchmark
```

This command will execute a series of benchmarks for different shuffle compression settings and I/O compression codecs, and save the results in the `data/` directory.

## 🧹 Maintenance

### Clean Data and Logs

To remove all generated data and log files:

```bash
make clean
```

## 📁 Project Structure

```
spark_io_explore/
├── docker-compose.yml          # Defines Spark cluster services
├── configs/                    # Spark configuration files
├── scripts/                    # Benchmark scripts
├── data/                       # Stores benchmark results and test data
├── logs/                       # Stores Spark and application logs
├── start_research_environment.sh # Script to start the Docker environment
├── Makefile                    # Defines project commands (benchmark, clean, etc.)
└── README.md                   # This file
```

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🙏 Acknowledgments

- Apache Spark community
- Open source contributors
