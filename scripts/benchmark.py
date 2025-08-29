from pyspark.sql import SparkSession
from sparkmeasure import StageMetrics
from pyspark.sql.functions import broadcast

def benchmark_join_with_broadcast(spark, df1, df2, join_cols):
    """Benchmarks a join operation with broadcasting."""
    print(f"\n--- Benchmarking join with broadcast ---")
    stagemetrics = StageMetrics(spark)
    stagemetrics.begin()
    df = df1.join(broadcast(df2), join_cols)
    df.count()
    stagemetrics.end()
    stagemetrics.print_report()

def benchmark_partitioned_read(spark, table_name, input_path, filter_condition):
    """Benchmarks reading from a partitioned table."""
    print(f"\n--- Benchmarking read from partitioned table: {table_name} ---")
    stagemetrics = StageMetrics(spark)
    stagemetrics.begin()
    df = spark.read.parquet(input_path).where(filter_condition)
    df.count()
    stagemetrics.end()
    stagemetrics.print_report()

def benchmark_bucketed_join(spark, df1, df2, join_cols):
    """Benchmarks a join operation on bucketed tables."""
    print(f"\n--- Benchmarking join on bucketed tables ---")
    stagemetrics = StageMetrics(spark)
    stagemetrics.begin()
    df = df1.join(df2, join_cols)
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

    spark = SparkSession.builder.appName("Spark IO Optimization Benchmark").getOrCreate()

    # --- Broadcasting ---
    table1_name = "store_sales"
    table1_path = f"/opt/spark/data/tpcds_parquet/{table1_name}"
    df1 = spark.read.parquet(table1_path)
    table2_name = "date_dim"
    table2_path = f"/opt/spark/data/tpcds_parquet/{table2_name}"
    df2 = spark.read.parquet(table2_path).withColumnRenamed("d_date_sk", "ss_sold_date_sk")
    join_cols = ["ss_sold_date_sk"]
    benchmark_join_with_broadcast(spark, df1, df2, join_cols)

    # --- Partitioning ---
    partitioned_table_path = "/opt/spark/data/tpcds_parquet/store_sales_partitioned"
    filter_condition = "ss_sold_date_sk = 2451545"
    benchmark_partitioned_read(spark, "store_sales_partitioned", partitioned_table_path, filter_condition)

    # Benchmark non-partitioned read for comparison
    non_partitioned_table_path = "/opt/spark/data/tpcds_parquet/store_sales"
    benchmark_read_non_partitioned(spark, "store_sales", non_partitioned_table_path, filter_condition)

    # --- Bucketing ---
    df1_bucketed_path = "/opt/spark/data/store_sales_bucketed"
    df1_bucketed = spark.read.parquet(df1_bucketed_path)
    df2_bucketed_path = "/opt/spark/data/item_bucketed"
    df2_bucketed = spark.read.parquet(df2_bucketed_path).withColumnRenamed("i_item_sk", "ss_item_sk")
    join_cols = ["ss_item_sk"]
    benchmark_bucketed_join(spark, df1_bucketed, df2_bucketed, join_cols)

    spark.stop()

if __name__ == "__main__":
    main()