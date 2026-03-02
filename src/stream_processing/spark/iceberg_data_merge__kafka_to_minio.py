from pyspark.sql import SparkSession
from src.common.env_config import EnvConfig

env_config = EnvConfig(env_path=".env",
    required_keys=["ICEBERG_WAREHOUSE_CATALOG", 
        "ICEBERG_DB", 
        "ICEBERG_TABLE", 
        "ICEBERG_TABLE_PATH", 
        "ICEBERG_CHECKPOINTLOCATION_PATH"
    ]
)

spark = SparkSession.builder \
    .appName("iceberg_rewrite") \
    .config("spark.sql.catalog.iceberg_catalog", "org.apache.iceberg.spark.SparkCatalog") \
    .config("spark.sql.catalog.iceberg_catalog.type", "hadoop") \
    .config("spark.sql.catalog.iceberg_catalog.warehouse", env_config.iceberg_warehouse_catalog) \
    .config("spark.sql.extensions", "org.apache.iceberg.spark.extensions.IcebergSparkSessionExtensions") \
    .getOrCreate()

spark.sql(f"SHOW TABLES IN {env_config.iceberg_db}").show()

spark.sql(f"""
CALL iceberg_catalog.system.rewrite_data_files(
    table => '{env_config.iceberg_table}',
    sort_order => 'dwr_created_at',
    options => map(
        'target-file-size-bytes', '52428800',
        'min-file-size-bytes', '41943040',
        'max-file-size-bytes', '62914560'
    )
)
""")

spark.stop()
