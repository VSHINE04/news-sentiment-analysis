"""Simple runtime test: create SparkSession, create/process DataFrame, convert to Pandas and back.

Run this with the project's venv python to verify Spark can start and handle DataFrames.
"""
import os
import sys
import traceback
from pyspark.sql import SparkSession


def run_test():
    python_executable = sys.executable
    # Make sure Spark uses the same Python interpreter
    os.environ['PYSPARK_PYTHON'] = python_executable
    os.environ['PYSPARK_DRIVER_PYTHON'] = python_executable

    spark = (
        SparkSession.builder
        .appName('TestSparkDataFrame')
        .master('local[1]')
        .config('spark.ui.enabled', 'false')
        .config('spark.driver.bindAddress', '127.0.0.1')
        .config('spark.driver.host', 'localhost')
        .config('spark.sql.execution.arrow.pyspark.enabled', 'false')
        .getOrCreate()
    )

    try:
        print('\n--- Spark session info ---')
        print('Spark app name:', spark.sparkContext.appName)
        print('Python executable:', python_executable)

        # Sample rows
        rows = [
            {'id': 1, 'text': 'hello world'},
            {'id': 2, 'text': 'apache spark'},
            {'id': 3, 'text': 'pandas conversion'},
        ]

        print('\nCreating DataFrame from Python list...')
        df = spark.createDataFrame(rows)
        print('DF count (should be 3):', df.count())

        print('\nDF show():')
        df.show()

        print('\nDF schema:')
        df.printSchema()

        # Simple transform: filter id > 1 and select text
        print("\nFilter id > 1 and select 'text':")
        df_filtered = df.filter(df['id'] > 1).select('text')
        df_filtered.show()

        # Convert to Pandas
        print('\nConverting Spark DataFrame to Pandas...')
        pdf = df.toPandas()
        print('Pandas head:')
        print(pdf.head())

        # Convert back to Spark
        print('\nConverting Pandas DataFrame back to Spark...')
        sdf2 = spark.createDataFrame(pdf)
        print('Back-converted Spark DF count (should be 3):', sdf2.count())

        print('\n✅ Spark DataFrame test completed successfully')
        return 0

    except Exception:
        print('\n❌ Spark DataFrame test failed:')
        traceback.print_exc()
        return 2

    finally:
        try:
            spark.stop()
            print('\nSpark session stopped')
        except Exception:
            pass


if __name__ == '__main__':
    sys.exit(run_test())
