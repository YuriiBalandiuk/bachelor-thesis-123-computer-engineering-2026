from pyspark.sql import SparkSession
from pyspark.sql.functions import (
    lit,
    col, 
    when,
    from_json, 
    to_timestamp, 
    trim, 
    from_utc_timestamp,
    current_timestamp,
)
from pyspark.sql.types import (
    StructType, 
    IntegerType, 
    DecimalType, 
    StringType
)

from src.common.env_config import EnvConfig

env_config = EnvConfig(env_path=".env",
    required_keys=["ICEBERG_WAREHOUSE_CATALOG", 
        "ICEBERG_DB", 
        "ICEBERG_TABLE", 
        "ICEBERG_TABLE_PATH", 
        "ICEBERG_CHECKPOINTLOCATION_PATH"
    ]
)

spark = (
    SparkSession.builder
    .appName("thingspeak__kafka_to_minio")
    .config("spark.sql.catalog.iceberg_catalog", "org.apache.iceberg.spark.SparkCatalog")
    .config("spark.sql.catalog.iceberg_catalog.type", "hadoop")
    .config("spark.sql.catalog.iceberg_catalog.warehouse", env_config.iceberg_warehouse_catalog)
    .getOrCreate()
)

conf = spark.sparkContext.getConf()
spark.sparkContext.setLogLevel("INFO")

spark.sql(f"""
CREATE DATABASE IF NOT EXISTS {env_config.iceberg_db}
""")

spark.sql(f"""
CREATE TABLE IF NOT EXISTS {env_config.iceberg_table} (
    channel_id INTEGER,
    entry_id INTEGER,
    created_at TIMESTAMP,
    ts_created_at TIMESTAMP,
    is_created BOOLEAN,
    temperature DECIMAL(18,4),
    humidity DECIMAL(18,4),
    pressure DECIMAL(18,4),
    air_co2 DECIMAL(18,4),
    luxmeter DECIMAL(18,4),
    moisture DECIMAL(18,4),
    particulate_matter_1_0 INTEGER,
    particulate_matter_2_5 INTEGER,
    particulate_matter_10 INTEGER,
    dwr_extracted_at TIMESTAMP,
    dwr_created_at TIMESTAMP,
    raw_payload STRING
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
    .selectExpr("CAST(value AS STRING) as raw_payload")
        .select(col("raw_payload"),
            from_json(col("raw_payload"), schema).alias("data")
    )
    .select("data.*", "raw_payload")
)

processed_df = parsed_df.select(

    trim(col("channel_id")).cast(IntegerType()).alias("channel_id"),
    trim(col("entry_id")).cast(IntegerType()).alias("entry_id"),

    to_timestamp(col("created_at")).alias("created_at"),
    from_utc_timestamp(col("created_at"), "America/New_York").alias("ts_created_at"),

    when(col("channel_id").isNotNull(), True).otherwise(False)
        .alias("is_created"),

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
        .alias("moisture"),
    
    when(col("channel_id") == 371428, col("field6").cast(IntegerType()))
        .otherwise(lit(None).cast(IntegerType()))
        .alias("particulate_matter_1_0"),

    when(col("channel_id") == 371428, col("field7").cast(IntegerType()))
        .otherwise(lit(None).cast(IntegerType()))
        .alias("particulate_matter_2_5"),
    
    when(col("channel_id") == 371428, col("field8").cast(IntegerType()))
        .otherwise(lit(None).cast(IntegerType()))
        .alias("particulate_matter_10"),
    
    to_timestamp(current_timestamp()).alias("dwr_extracted_at"),
    to_timestamp(col("created_at")).alias("dwr_created_at"),

    col("raw_payload")
)


query = (
    processed_df.writeStream
    .format("iceberg")
    .outputMode("append")
    .option("path", env_config.iceberg_table_path) 
    .option("checkpointLocation", env_config.iceberg_checkpointlocation_path)
    .start()
)

query.awaitTermination()
