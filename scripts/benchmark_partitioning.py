from pyspark.sql import SparkSession
from sparkmeasure import StageMetrics

def benchmark_partitioned_read(spark, table_name, input_path, filter_condition):
    """Benchmarks reading from a partitioned table."""
    print(f"\n--- Benchmarking read from partitioned table: {table_name} ---")
    stagemetrics = StageMetrics(spark)
    stagemetrics.begin()
    df = spark.read.parquet(input_path).where(filter_condition)
    df.count()
    stagemetrics.end()
    stagemetrics.print_report()

def benchmark_read_non_partitioned(spark, table_name, input_path, filter_condition):
    """Benchmarks reading from a non-partitioned table with a filter."""
    print(f"\n--- Benchmarking read from non-partitioned table: {table_name} ---")
    stagemetrics = StageMetrics(spark)
    stagemetrics.begin()
    df = spark.read.parquet(input_path).where(filter_condition)
    df.count()
    stagemetrics.end()
    stagemetrics.print_report()

def main():
    spark = SparkSession.builder.appName("Spark Partitioning Benchmarks").getOrCreate()

    filter_condition = "ss_sold_date_sk = 2451545"

    # --- Partitioning ---
    partitioned_table_path = "/opt/spark/data/tpcds_parquet/store_sales_partitioned"
    benchmark_partitioned_read(spark, "store_sales_partitioned", partitioned_table_path, filter_condition)

    # Benchmark non-partitioned read for comparison
    non_partitioned_table_path = "/opt/spark/data/tpcds_parquet/store_sales"
    benchmark_read_non_partitioned(spark, "store_sales", non_partitioned_table_path, filter_condition)

    spark.stop()

if __name__ == "__main__":
    main()
