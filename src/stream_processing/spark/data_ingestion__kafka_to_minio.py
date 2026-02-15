import os
from dotenv import load_dotenv

from pyspark.sql import SparkSession
from pyspark.sql.functions import col, from_json, to_timestamp
from pyspark.sql.types import StructType, StringType, IntegerType, DecimalType

load_dotenv(".env")

spark = (
    SparkSession.builder
    .appName("KafkaToMinIOExample")
    .config("spark.hadoop.fs.s3a.endpoint", os.getenv("S3A_ENDPOINT"))
    .config("spark.hadoop.fs.s3a.access.key", os.getenv("ACCESS_KEY"))
    .config("spark.hadoop.fs.s3a.secret.key", os.getenv("SECRET_KEY"))
    .config("spark.hadoop.fs.s3a.path.style.access", "true")
    .config("spark.hadoop.fs.s3a.impl", "org.apache.hadoop.fs.s3a.S3AFileSystem")
    # .config("spark.hadoop.fs.s3a.aws.credentials.provider", "org.apache.hadoop.fs.s3a.SimpleAWSCredentialsProvider") 
    .getOrCreate()
)

spark.sparkContext.setLogLevel("WARN")

schema = (
    StructType()
    .add("channel_id", IntegerType())
    .add("created_at", StringType())
    .add("entry_id", IntegerType())
    .add("field1", DecimalType())
    .add("field2", DecimalType())
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

processed_df = (
    parsed_df
    .withColumn("dwr_created_at", to_timestamp(col("created_at")))
)

query = (
    processed_df.writeStream
    .format("parquet")
    .option("path", os.getenv("S3_BUCKED"))
    .option("checkpointLocation", os.getenv("S3_BUCKED_CHECKPOINTLOCATION"))
    .partitionBy("channel_id")
    .outputMode("append")
    .start()
)

query.awaitTermination()