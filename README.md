# Spark I/O Performance Research Project

A comprehensive research environment for exploring and benchmarking Apache Spark I/O optimization techniques, including shuffle operations, S3 integration, network I/O, and memory management.

## 🎯 Research Objectives

This project investigates the key I/O bottlenecks in Apache Spark and evaluates various optimization strategies:

- **Shuffle I/O Optimization**: External shuffle service, compression algorithms, spill management
- **S3 I/O Optimization**: S3A committers, multipart uploads, S3 Select pushdown
- **Network I/O Optimization**: RDMA, zero-copy techniques, compression
- **Memory I/O Optimization**: Off-heap memory, caching strategies, memory management
- **File Format Optimization**: Parquet, ORC, compression algorithms

## 🏗️ Architecture

The research environment consists of:

- **Spark Cluster**: 1 master + 2 worker nodes (Docker containers)
- **Jupyter Lab**: Interactive notebook environment for experimentation
- **Benchmarking Tools**: Automated performance testing scripts
- **Configuration Profiles**: Pre-configured optimization strategies
- **Research Documentation**: Comprehensive literature review and findings

## 🚀 Quick Start

### Prerequisites

- Docker and Docker Compose
- Python 3.10+ (for local development)
- uv (Python package manager) - will be auto-installed if missing
- 8GB+ RAM available for the cluster

### 1. Clone and Setup

```bash
git clone <repository-url>
cd spark_io_explore
chmod +x start_research_environment.sh
```

### 2. Python Environment Setup (Optional)

The project uses `uv` for fast Python dependency management. If you want to work locally:

```bash
# Install uv (if not already installed)
curl -LsSf https://astral.sh/uv/install.sh | sh

# Install dependencies
uv sync

# Activate virtual environment
source .venv/bin/activate  # On Unix/macOS
# or
.venv\Scripts\activate     # On Windows
```

### 3. Start the Environment

```bash
./start_research_environment.sh
```

This will:
- Start a 3-node Spark cluster
- Launch Jupyter Lab
- Set up all necessary directories and permissions

### 4. Access the Environment

- **Jupyter Lab**: http://localhost:8888
- **Spark Master UI**: http://localhost:8080
- **Spark Master URL**: `spark://localhost:7077`

## 📊 Running Benchmarks

### Automated Benchmarking

Run comprehensive I/O performance tests:

```bash
# Run the main benchmark script
python scripts/io_benchmark.py

# Or run from within the cluster
docker exec -it spark-master python /opt/bitnami/spark/scripts/io_benchmark.py
```

### Interactive Research

Open the Jupyter notebook for interactive experimentation:

```bash
# Access Jupyter Lab at http://localhost:8888
# Open: notebooks/spark_io_research.ipynb
```

## 🔬 Research Areas

### 1. Shuffle I/O Performance

**Current Challenges:**
- Shuffle spill to disk causing I/O overhead
- Network transfer bottlenecks between nodes
- Serialization/deserialization overhead

**Optimization Strategies:**
- External shuffle service
- Compression algorithms (LZ4, Snappy, Zstandard)
- Memory management and spill prediction
- Tungsten project optimizations

### 2. S3 Integration Performance

**Current Challenges:**
- S3 eventual consistency model
- Network latency for cloud storage
- Data transfer costs

**Optimization Strategies:**
- S3A committers for atomic writes
- Multipart uploads for large files
- S3 Select for pushdown filtering
- Local buffering strategies

### 3. Network I/O Optimization

**Current Challenges:**
- Bandwidth limitations between nodes
- TCP/IP protocol overhead
- Round-trip latency

**Optimization Strategies:**
- RDMA (Remote Direct Memory Access)
- Zero-copy data transfer
- Network-aware task scheduling
- Compression for bandwidth reduction

### 4. Memory and Storage Optimization

**Current Challenges:**
- JVM memory pressure and GC pauses
- Memory fragmentation
- Inefficient allocation strategies

**Optimization Strategies:**
- Off-heap memory management
- Memory pools and efficient allocation
- Intelligent caching policies
- Memory-aware scheduling

## 📁 Project Structure

```
spark_io_explore/
├── docker-compose.yml          # Spark cluster configuration
├── configs/                    # Spark configuration files
│   └── spark-defaults.conf    # I/O optimization settings
├── scripts/                    # Benchmarking scripts
│   └── io_benchmark.py        # Main benchmark script
├── notebooks/                  # Jupyter notebooks
│   └── spark_io_research.ipynb # Interactive research notebook
├── research/                   # Research documentation
│   └── spark_io_optimization_research.md
├── data/                       # Benchmark results and test data
├── logs/                       # Spark and application logs
├── requirements.txt            # Python dependencies
├── start_research_environment.sh # Startup script
└── README.md                   # This file
```

## ⚙️ Configuration Profiles

The project includes several pre-configured optimization profiles:

### Default Configuration
- Basic Spark settings
- Standard memory management
- Default compression settings

### Optimized Shuffle
- External shuffle service enabled
- LZ4 compression for shuffle data
- Optimized spill management

### High Memory
- Increased memory fractions
- Optimized storage memory allocation
- Reduced spilling to disk

### Compression Heavy
- Snappy compression for Parquet
- Vectorized reading enabled
- Optimized file format settings

### Network Optimized
- Extended network timeouts
- Optimized RPC settings
- Better heartbeat management

## 📈 Benchmarking Metrics

The benchmarking system measures:

- **Execution Time**: Total operation duration
- **Throughput**: Rows processed per second
- **Memory Usage**: Peak memory consumption
- **Network I/O**: Data transfer volume
- **Disk I/O**: Read/write operation counts
- **Shuffle Performance**: Cross-node data movement efficiency

## 🔍 Expected Performance Improvements

Based on research and industry experience:

- **Shuffle Operations**: 20-40% improvement
- **File I/O**: 30-50% improvement with columnar formats
- **Memory Usage**: 15-25% reduction
- **Network Transfer**: 25-35% improvement with compression

## 📚 Research References

The project includes comprehensive research on:

- Academic papers on Spark performance
- Industry white papers and case studies
- Performance optimization best practices
- Emerging technologies and future directions

## 🛠️ Development and Customization

### Python Environment Management with uv

The project uses `uv` for fast dependency management:

```bash
# Install dependencies
uv sync

# Install with development extras
uv sync --extra dev

# Install with all extras
uv sync --all-extras

# Add new dependency
uv add package_name

# Add development dependency
uv add --dev package_name

# Remove dependency
uv remove package_name

# Update dependencies
uv lock --upgrade

# Show dependency tree
uv tree

# Run commands in virtual environment
uv run python script.py
uv run pytest
uv run black .
```

### Adding New Optimization Strategies

1. **Configuration**: Add new settings to `configs/spark-defaults.conf`
2. **Benchmarking**: Extend `scripts/io_benchmark.py` with new tests
3. **Notebooks**: Add research cells to the Jupyter notebook
4. **Documentation**: Update research findings in the `research/` directory

### Custom Workloads

Modify the benchmark script to test your specific use cases:

```python
# Add custom operations
def benchmark_custom_workload(df):
    # Your custom benchmark logic here
    pass
```

## 🐛 Troubleshooting

### Common Issues

1. **Port Conflicts**: Ensure ports 8080, 7077, and 8888 are available
2. **Memory Issues**: Increase Docker memory allocation if needed
3. **Slow Startup**: The first startup may take several minutes for image downloads

### Debug Commands

```bash
# Check service status
docker-compose ps

# View logs
docker-compose logs -f spark-master
docker-compose logs -f jupyter

# Restart services
docker-compose restart

# Clean restart
docker-compose down
docker-compose up -d
```

## 🤝 Contributing

Contributions are welcome! Areas for contribution:

- New optimization strategies
- Additional benchmark scenarios
- Performance analysis tools
- Research documentation updates
- Bug fixes and improvements

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🙏 Acknowledgments

- Apache Spark community for the excellent framework
- Research community for performance optimization insights
- Open source contributors for benchmarking tools and libraries

---

**Happy researching! 🚀**

For questions or contributions, please open an issue or pull request.
