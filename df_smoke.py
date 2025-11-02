import os
import sys
from pyspark.sql import SparkSession
from pyspark.sql.types import StructType, StructField, StringType, IntegerType

python_executable = sys.executable
os.environ['PYSPARK_PYTHON'] = python_executable
os.environ['PYSPARK_DRIVER_PYTHON'] = python_executable

spark = (
	SparkSession.builder
	.appName('DfSmoke')
	.master('local[1]')
	.config('spark.ui.enabled', 'false')
	.config('spark.driver.bindAddress', '127.0.0.1')
	.config('spark.driver.host', 'localhost')
	.config('spark.sql.execution.arrow.pyspark.enabled', 'false')
	.config('spark.python.worker.reuse', 'false')
	.config('spark.sql.adaptive.enabled', 'false')
	.getOrCreate()
)

rows = [{'a': 'x', 'b': 1}, {'a': 'y', 'b': 2}]
schema = StructType([
	StructField('a', StringType(), True),
	StructField('b', IntegerType(), True),
])

data_rdd = spark.sparkContext.parallelize(rows)
df = spark.createDataFrame(data_rdd, schema=schema)
print('COUNT=', df.count())

spark.stop()
