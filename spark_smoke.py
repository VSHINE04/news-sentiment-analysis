import os
import sys
from pyspark.sql import SparkSession

# Ensure Spark uses the same Python interpreter
python_executable = sys.executable
os.environ['PYSPARK_PYTHON'] = python_executable
os.environ['PYSPARK_DRIVER_PYTHON'] = python_executable

spark = (
    SparkSession.builder
    .appName('SparkSmoke')
    .master('local[1]')
    .config('spark.ui.enabled', 'false')
    .config('spark.driver.bindAddress', '127.0.0.1')
    .config('spark.driver.host', 'localhost')
    .getOrCreate()
)

print('COUNT=', spark.range(10).count())

spark.stop()
