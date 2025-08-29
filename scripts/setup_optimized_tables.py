
from pyspark.sql import SparkSession

def main():
    spark = SparkSession.builder.appName("Setup Optimized Tables").getOrCreate()

    # --- Partitioning ---
    table_name = "store_sales"
    input_path = f"/opt/spark/data/tpcds_parquet/{table_name}"
    partitioned_table_path = "/opt/spark/data/tpcds_parquet/store_sales_partitioned"
    df = spark.read.parquet(input_path)
    df.write.mode("overwrite").partitionBy("ss_sold_date_sk").parquet(partitioned_table_path)
    print(f"Successfully created partitioned table: {partitioned_table_path}")

    # --- Bucketing ---
    spark.sql("CREATE DATABASE IF NOT EXISTS tpcds")
    spark.sql("USE tpcds")
    df.write.mode("overwrite").bucketBy(4, "ss_item_sk").sortBy("ss_item_sk").option("path", "/opt/spark/data/store_sales_bucketed").saveAsTable("store_sales_bucketed")
    print("Successfully created bucketed table: store_sales_bucketed")
    item_df = spark.read.parquet("/opt/spark/data/tpcds_parquet/item")
    item_df.write.mode("overwrite").bucketBy(4, "i_item_sk").sortBy("i_item_sk").option("path", "/opt/spark/data/item_bucketed").saveAsTable("item_bucketed")
    print("Successfully created bucketed table: item_bucketed")

    spark.stop()

if __name__ == "__main__":
    main()
