import os
from dotenv import load_dotenv

from pyspark.sql import SparkSession
from pyspark.sql.functions import (
    lit,
    col, 
    when,
    from_json, 
    to_timestamp, 
    trim, 
    from_utc_timestamp,
)
from pyspark.sql.types import (
    StructType, 
    IntegerType, 
    DecimalType, 
    StringType
)

load_dotenv(".env")

spark = (
    SparkSession.builder
    .appName("KafkaToMinIOExample")
    .config("spark.sql.catalog.iceberg_catalog", "org.apache.iceberg.spark.SparkCatalog")
    .config("spark.sql.catalog.iceberg_catalog.type", "hadoop")
    .config("spark.sql.catalog.iceberg_catalog.warehouse", os.getenv("ICEBERG_CATALOG_WAREHOUSE"))
    .getOrCreate()
)

conf = spark.sparkContext.getConf()
spark.sparkContext.setLogLevel("INFO")

spark.sql(f"""
CREATE DATABASE IF NOT EXISTS {os.getenv("ICEBERG_DB")}
""")

spark.sql(f"""
CREATE TABLE IF NOT EXISTS { os.getenv("ICEBERG_TABLE") } (
    channel_id INTEGER,
    entry_id INTEGER,
    created_at TIMESTAMP,
    ts_created_at TIMESTAMP,
    temperature DECIMAL(18,4),
    humidity DECIMAL(18,4),
    pressure DECIMAL(18,4),
    air_co2 DECIMAL(18,4),
    luxmeter DECIMAL(18,4),
    moisure DECIMAL(18,4),
    particulate_matter_1_0 INTEGER,
    particulate_matter_2_5 INTEGER,
    particulate_matter_10 INTEGER,
    dwr_created_at TIMESTAMP
)
USING iceberg
PARTITIONED BY (channel_id);
""")

schema = (
    StructType()
    .add("channel_id", StringType())
    .add("entry_id", StringType())
    .add("created_at", StringType())
    .add("field1", StringType())
    .add("field2", StringType())
    .add("field3", StringType())
    .add("field4", StringType())
    .add("field5", StringType())
    .add("field6", StringType())
    .add("field7", StringType())
    .add("field8", StringType())
)

kafka_df = (
    spark.readStream
    .format("kafka")
    .option("kafka.bootstrap.servers", "kafka1:9092,kafka2:9092")
    .option("subscribe", "thingspeak-topic")
    .option("startingOffsets", "earliest")
    .load()
)

parsed_df = (
    kafka_df
    .selectExpr("CAST(value AS STRING)")
    .select(from_json(col("value"), schema).alias("data"))
    .select("data.*")
)

processed_df = parsed_df.select(

    trim(col("channel_id")).cast(IntegerType()).alias("channel_id"),
    trim(col("entry_id")).cast(IntegerType()).alias("entry_id"),

    to_timestamp(col("created_at")).alias("created_at"),
    from_utc_timestamp(col("created_at"), "America/New_York").alias("ts_created_at"),

    trim(col("field1")).cast(DecimalType(18,4)).alias("temperature"),
    trim(col("field2")).cast(DecimalType(18,4)).alias("humidity"),

    when(col("channel_id") == 3217660, col("field3").cast(DecimalType(18,4)))
        .otherwise(col("field4").cast(DecimalType(18,4)))
        .alias("pressure"),
    
    when(col("channel_id") == 371428, col("field3").cast(DecimalType(18,4)))
        .otherwise(lit(None).cast(DecimalType(18,4)))
        .alias("air_co2"),

    when(col("channel_id") == 3217660, col("field4").cast(DecimalType(18,4)))
        .otherwise(lit(None).cast(DecimalType(18,4)))
        .alias("luxmeter"),

    when(col("channel_id") == 3217660, col("field5").cast(DecimalType(18,4)))
        .otherwise(lit(None).cast(DecimalType(18,4)))
        .alias("moisure"),
    
    when(col("channel_id") == 371428, col("field6").cast(IntegerType()))
        .otherwise(lit(None).cast(IntegerType()))
        .alias("particulate_matter_1_0"),

    when(col("channel_id") == 371428, col("field7").cast(IntegerType()))
        .otherwise(lit(None).cast(IntegerType()))
        .alias("particulate_matter_2_5"),
    
    when(col("channel_id") == 371428, col("field8").cast(IntegerType()))
        .otherwise(lit(None).cast(IntegerType()))
        .alias("particulate_matter_10"),
    
    to_timestamp(col("created_at")).alias("dwr_created_at")
)


query = (
    processed_df.writeStream
    .format("iceberg")
    .outputMode("append")
    .option("path", os.getenv("ICEBERG_TABLE_PATH"))
    .option("checkpointLocation", os.getenv("ICEBERG_CHECKPOINTLOCATION_PATH"))
    .start()
)

query.awaitTermination()
