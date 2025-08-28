#!/usr/bin/env python3
"""
Cluster Spark I/O Benchmark - Submits the job to the Spark master.
"""

import time
import json
import logging
from datetime import datetime
import random
import string
import os
import sys
from pyspark.sql import SparkSession
from pyspark.sql.functions import col, count, sum as spark_sum, avg as spark_avg, max as spark_max, min as spark_min
from pyspark.sql.types import StructType, StructField, StringType, IntegerType, DoubleType

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def generate_test_data(num_rows=50000):
    """Generate test data for benchmarking."""
    data = []
    for i in range(num_rows):
        data.append(( 
            i,
            ''.join(random.choices(string.ascii_letters, k=10)),
            random.uniform(0, 10000),
            random.choice(['Category_A', 'Category_B', 'Category_C', 'Category_D', 'Category_E']),
            datetime.now().isoformat()
        ))
    return data

def run_benchmark(spark: SparkSession, benchmark_type: str, compression_codec: str = None):
    """Run I/O benchmark on the cluster."""
    benchmark_name = f"Cluster Spark I/O Performance Benchmark - {benchmark_type}"
    if compression_codec:
        benchmark_name += f" ({compression_codec.upper()} Codec)"
    print(f"🚀 {benchmark_name}")
    print("=" * 70)

    try:
        # Create data directory
        os.makedirs("/opt/spark/data", exist_ok=True)

        # Generate test data
        print("📊 Generating test data...")
        data = generate_test_data(50000)
        schema = StructType([
            StructField("id", IntegerType(), False),
            StructField("name", StringType(), True),
            StructField("value", DoubleType(), True),
            StructField("category", StringType(), True),
            StructField("timestamp", StringType(), True)
        ])

        df = spark.createDataFrame(data, schema)
        print(f"✅ Data created: {df.count():,} rows")

        # Test 1: Basic operations (no shuffle)
        print("\n🧪 Test 1: Basic operations (no shuffle)...")
        start = time.time()
        filtered = df.filter(col("value") > 5000).count()
        basic_time = time.time() - start
        print(f"   Filter > 5000: {filtered:,} rows in {basic_time:.2f}s")

        # Test 2: Shuffle operations
        print("\n🧪 Test 2: Shuffle operations...")
        start = time.time()
        grouped = df.groupBy("category").agg(
            count("*" ).alias("count"),
            spark_avg("value").alias("avg_value"),
            spark_sum("value").alias("sum_value")
        ).collect()
        shuffle_time = time.time() - start
        print(f"   GroupBy + aggregations: {len(grouped)} groups in {shuffle_time:.2f}s")

        # Test 3: Complex shuffle with repartitioning
        print("\n🧪 Test 3: Complex shuffle with repartitioning...")
        start = time.time()
        repartitioned = df.repartition(5, "category")
        complex_grouped = repartitioned.groupBy("category").agg(
            spark_max("value").alias("max_value"),
            spark_min("value").alias("min_value"),
            spark_avg("value").alias("avg_value")
        ).collect()
        complex_time = time.time() - start
        print(f"   Repartition + GroupBy: {len(complex_grouped)} groups in {complex_time:.2f}s")

        # Test 4: File I/O operations
        print("\n🧪 Test 4: File I/O operations...")

        # Write Parquet
        start = time.time()
        output_path = "/opt/spark/data/test_parquet"
        if compression_codec:
            output_path = f"/opt/spark/data/test_parquet_{compression_codec}"
        df.write.mode("overwrite").parquet(output_path)
        write_time = time.time() - start
        print(f"   Parquet write ({compression_codec if compression_codec else 'default'}): {write_time:.2f}s")

        # Read Parquet
        start = time.time()
        read_df = spark.read.schema(schema).parquet(output_path)
        read_count = read_df.count()
        read_time = time.time() - start
        print(f"   Parquet read ({compression_codec if compression_codec else 'default'}): {read_count:,} rows in {read_time:.2f}s")

        # Test 5: Memory operations
        print("\n🧪 Test 5: Memory operations...")
        start = time.time()
        cached_df = df.cache()
        cached_count = cached_df.count()  # Force caching
        cache_time = time.time() - start
        print(f"   Cache + count: {cached_count:,} rows in {cache_time:.2f}s")

        # Test cached read
        start = time.time()
        cached_result = cached_df.filter(col("value") > 7000).count()
        cached_read_time = time.time() - start
        print(f"   Cached filter: {cached_result:,} rows in {cached_read_time:.2f}s")

        # Results summary
        total_time = basic_time + shuffle_time + complex_time + write_time + read_time + cache_time + cached_read_time

        print(f"\n📊 Benchmark Results Summary:")
        print(f"   Total time: {total_time:.2f}s")
        print(f"   Basic operations: {basic_time:.2f}s")
        print(f"   Simple shuffle: {shuffle_time:.2f}s")
        print(f"   Complex shuffle: {complex_time:.2f}s")
        print(f"   File write: {write_time:.2f}s")
        print(f"   File read: {read_time:.2f}s")
        print(f"   Memory cache: {cache_time:.2f}s")
        print(f"   Cached read: {cached_read_time:.2f}s")

        # Performance insights
        print(f"\n💡 Performance Insights:")
        print(f"   Shuffle overhead: {(shuffle_time + complex_time) / total_time * 100:.1f}% of total time")
        print(f"   I/O overhead: {(write_time + read_time) / total_time * 100:.1f}% of total time")
        print(f"   Memory benefit: {(basic_time - cached_read_time) / basic_time * 100:.1f}% faster with caching")

        # Save results
        results = {
            "timestamp": datetime.now().isoformat(),
            "benchmark_type": benchmark_type,
            "compression_codec": compression_codec,
            "total_time": total_time,
            "operations": {
                "basic": basic_time,
                "simple_shuffle": shuffle_time,
                "complex_shuffle": complex_time,
                "write": write_time,
                "read": read_time,
                "cache": cache_time,
                "cached_read": cached_read_time
            },
            "rows_processed": df.count(),
            "insights": {
                "shuffle_overhead_percent": (shuffle_time + complex_time) / total_time * 100,
                "io_overhead_percent": (write_time + read_time) / total_time * 100,
                "memory_benefit_percent": (basic_time - cached_read_time) / basic_time * 100
            }
        }

        output_filename = f"benchmark_{benchmark_type.replace(' ', '_').lower()}"
        if compression_codec:
            output_filename += f"_{compression_codec.lower()}"
        output_filename += ".json"
        output_filepath = f"/opt/spark/data/{output_filename}"

        with open(output_filepath, "w") as f:
            json.dump(results, f, indent=2)
            f.flush()
            os.fsync(f.fileno())

        print(f"\n✅ Results saved to {output_filepath}")

        # Cleanup
        cached_df.unpersist()

    except Exception as e:
        print(f"❌ Benchmark failed: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1) # Exit with error code

if __name__ == "__main__":
    spark = SparkSession.builder.getOrCreate()
    
    # Parse arguments
    if len(sys.argv) < 2:
        print("Usage: unified_benchmark.py <benchmark_type> [compression_codec]")
        sys.exit(1)
    
    benchmark_type = sys.argv[1]
    compression_codec = sys.argv[2] if len(sys.argv) > 2 else None

    run_benchmark(spark, benchmark_type, compression_codec)
