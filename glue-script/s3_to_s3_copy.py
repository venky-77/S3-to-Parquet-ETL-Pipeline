import sys
from awsglue.transforms import *
from awsglue.utils import getResolvedOptions
from pyspark.context import SparkContext
from awsglue.context import GlueContext
from awsglue.job import Job

## @params: [JOB_NAME]
args = getResolvedOptions(sys.argv, ['JOB_NAME'])

# Source S3 bucket (input data)
BUCKET_SRC = "s3a://storm-source-data-dumps-2026/sample_data/landing_zone_data/"

# Initialize Spark + Glue Context
sc = SparkContext()
glueContext = GlueContext(sc)
spark = glueContext.spark_session

# Initialize Glue Job
job = Job(glueContext)
job.init(args['JOB_NAME'], args)

# 🔹 Step 1: Read CSV from S3
df = (spark.read
      .option("header", True)        # First row as header
      .option("inferSchema", True)   # Auto-detect datatypes
      .csv(BUCKET_SRC))              # Path in S3

# 🔹 Step 2: Drop unwanted columns
df = df.drop("Phone 2", "Subscription")

# 🔹 Step 3: Write cleaned CSV back to another S3 location
df.write.parquet("s3a://storm-source-data-dumps-2026/sample_data/derived_data/",
             header=True,
             mode="overwrite")

# Commit job (important in AWS Glue)
job.commit()