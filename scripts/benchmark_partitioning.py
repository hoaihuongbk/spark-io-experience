from pyspark.sql import SparkSession
from sparkmeasure import StageMetrics
import json

def extract_metrics(stagemetrics_report):
    """Extracts relevant metrics from sparkmeasure report."""
    metrics = {}
    if stagemetrics_report is None:
        return metrics

    # Directly extract top-level aggregated metrics
    metrics['totalDuration'] = stagemetrics_report.get('elapsedTime', 0) / 1000 # Convert ms to seconds
    metrics['executorRunTime'] = stagemetrics_report.get('executorRunTime', 0) / 1000 # Convert ms to seconds
    metrics['bytesRead'] = stagemetrics_report.get('bytesRead', 0) # Bytes
    metrics['numTasks'] = stagemetrics_report.get('numTasks', 0) # Add numTasks
    metrics['recordsRead'] = stagemetrics_report.get('recordsRead', 0) # Add recordsRead

    # These are often found in taskMetrics, but might be aggregated differently
    # Let's try to find them in the first task metric if available
    if 'taskMetrics' in stagemetrics_report and stagemetrics_report['taskMetrics']:
        first_task_metrics = stagemetrics_report['taskMetrics'][0]
        metrics['numFilesRead'] = first_task_metrics.get('inputMetrics', {}).get('numFilesRead', 0)
        metrics['numPartitionsRead'] = first_task_metrics.get('inputMetrics', {}).get('numPartitionsRead', 0)
    else:
        metrics['numFilesRead'] = 0
        metrics['numPartitionsRead'] = 0

    return metrics

def benchmark_partitioned_read(spark, table_name, input_path, filter_condition):
    """Benchmarks reading from a partitioned table."""
    print(f"\n--- Benchmarking read from partitioned table: {table_name} ---")
    stagemetrics = StageMetrics(spark)
    stagemetrics.begin()
    df = spark.read.parquet(input_path).where(filter_condition)
    df.count()
    report = stagemetrics.end()
    stagemetrics.print_report() # Keep for stdout visibility
    return extract_metrics(report)

def benchmark_read_non_partitioned(spark, table_name, input_path, filter_condition):
    """Benchmarks reading from a non-partitioned table with a filter."""
    print(f"\n--- Benchmarking read from non-partitioned table: {table_name} ---")
    stagemetrics = StageMetrics(spark)
    stagemetrics.begin()
    df = spark.read.parquet(input_path).where(filter_condition)
    df.count()
    report = stagemetrics.end()
    stagemetrics.print_report() # Keep for stdout visibility
    return extract_metrics(report)

def main():
    spark = SparkSession.builder \
        .appName("Spark Partitioning Benchmarks") \
        .config("spark.sql.parquet.filterPushdown", "true") \
        .getOrCreate()

    filter_condition = "ss_sold_date_sk = 2451545"

    # --- Partitioning ---
    partitioned_table_path = "/opt/spark/data/tpcds_parquet/store_sales_partitioned"
    partitioned_metrics = benchmark_partitioned_read(spark, "store_sales_partitioned", partitioned_table_path, filter_condition)

    # Benchmark non-partitioned read for comparison
    non_partitioned_table_path = "/opt/spark/data/tpcds_parquet/store_sales"
    non_partitioned_metrics = benchmark_read_non_partitioned(spark, "store_sales", non_partitioned_table_path, filter_condition)

    spark.stop()

if __name__ == "__main__":
    main()
