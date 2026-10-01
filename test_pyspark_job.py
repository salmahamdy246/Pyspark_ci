import pytest
from pyspark.sql import SparkSession
from pyspark.sql.types import StructType, StructField, StringType, DoubleType
from pyspark_job import clean_data

@pytest.fixture(scope="session")
def spark():
    session = SparkSession.builder \
        .master("local[1]") \
        .appName("PySpark-CI-Tests") \
        .getOrCreate()
    yield session
    session.stop()

def test_clean_data(spark):
    schema = StructType([
        StructField("id", StringType(), True),
        StructField("name", StringType(), True),
        StructField("amount", DoubleType(), True),
    ])

    input_data = [
        ("1", "Alice", 100.0),   # Valid record
        ("2", "Bob", 0.0),       # Invalid: amount <= 0
        ("3", "Charlie", -50.0), # Invalid: amount <= 0
        ("4", None, 200.0),      # Invalid: NULL name
        ("5", "Eva", 50.0)       # Valid record
    ]

    input_df = spark.createDataFrame(input_data, schema=schema)
    result_df = clean_data(input_df)
    results = result_df.collect()

    assert len(results) == 2

    names = [row["name"] for row in results]
    assert "Alice" in names
    assert "Eva" in names
    assert "Bob" not in names
    assert "Charlie" not in names
    assert None not in names

    alice_row = next(r for r in results if r["name"] == "Alice")
    eva_row = next(r for r in results if r["name"] == "Eva")

    assert pytest.approx(alice_row["amount_with_tax"], 0.01) == 120.0
    assert pytest.approx(eva_row["amount_with_tax"], 0.01) == 60.0