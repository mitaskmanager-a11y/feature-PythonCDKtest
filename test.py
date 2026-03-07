"""
AWS Glue PySpark Job: Convert CSV files from S3 to Parquet in S3

Purpose:
- Read CSV data from an S3 input path
- Convert it to Parquet format
- Write the output back to an S3 output path

Notes for code review:
- This version is parameterized for reusable deployment across environments
- Includes basic logging and comments for maintainability
- Uses Spark DataFrame API for clarity and flexibility
"""

import sys
from awsglue.utils import getResolvedOptions
from awsglue.context import GlueContext
from awsglue.job import Job
from pyspark.context import SparkContext


# ---------------------------------------------------------------------------
# Read job arguments passed from AWS Glue job parameters
# Expected example:
# --JOB_NAME csv_to_parquet_job
# --INPUT_PATH s3://my-bucket/raw/input/
# --OUTPUT_PATH s3://my-bucket/curated/output/
# --WRITE_MODE overwrite
# ---------------------------------------------------------------------------
args = getResolvedOptions(
    sys.argv,
    ["JOB_NAME", "INPUT_PATH", "OUTPUT_PATH", "WRITE_MODE"]
)

job_name = args["JOB_NAME"]
input_path = args["INPUT_PATH"]
output_path = args["OUTPUT_PATH"]
write_mode = args["WRITE_MODE"]  # common values: overwrite / append


# ---------------------------------------------------------------------------
# Initialize Spark / Glue contexts
# ---------------------------------------------------------------------------
sc = SparkContext()
glue_context = GlueContext(sc)
spark = glue_context.spark_session
job = Job(glue_context)
job.init(job_name, args)


# ---------------------------------------------------------------------------
# Log input parameters for operational visibility
# ---------------------------------------------------------------------------
logger = glue_context.get_logger()
logger.info(f"Starting Glue job: {job_name}")
logger.info(f"Input path  : {input_path}")
logger.info(f"Output path : {output_path}")
logger.info(f"Write mode  : {write_mode}")


# ---------------------------------------------------------------------------
# Read CSV files from S3
# Options:
# - header=True       -> first row treated as column names
# - inferSchema=True  -> Spark infers datatypes automatically
#
# Note:
# For production-grade pipelines with strict schema control, replace
# inferSchema=True with an explicit schema definition.
# ---------------------------------------------------------------------------
df = (
    spark.read
    .option("header", "true")
    .option("inferSchema", "true")
    .csv(input_path)
)

logger.info(f"Source record count: {df.count()}")
logger.info("CSV read completed successfully")


# ---------------------------------------------------------------------------
# Optional: apply transformations here if needed
# Example placeholders:
# - trim column names
# - cast datatypes
# - remove duplicates
# - add audit columns
# ---------------------------------------------------------------------------
# df = df.dropDuplicates()


# ---------------------------------------------------------------------------
# Write output as Parquet to S3
#
# Parquet advantages:
# - columnar storage
# - better compression
# - faster reads for analytics tools such as Athena
# ---------------------------------------------------------------------------
(
    df.write
    .mode(write_mode)
    .parquet(output_path)
)

logger.info("Parquet write completed successfully")
logger.info(f"Data written to: {output_path}")


# ---------------------------------------------------------------------------
# Commit the Glue job
# ---------------------------------------------------------------------------
job.commit()
logger.info(f"Glue job completed successfully: {job_name}")


