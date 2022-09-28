import csv
import pyspark
import pyspark.sql.functions as F
import pyspark.sql.types as T


spark = (pyspark.sql.SparkSession.builder
         .appName("test_df")
         .master("local[6]")
         .getOrCreate()
         )
spark.conf.set("spark.sql.shuffle.partitions", "5")

schema = T.StructType([
    T.StructField("firstname", T.StringType(), True),
    T.StructField("lastname", T.StringType(), True)
])


# https://docs.databricks.com/spark/latest/spark-sql/language-manual/sql-ref-datatypes.html
schema = '''
firstname STRING,
lastname STRING
'''
data = [
    ("Rick", "Sanchez"),
    ("Morty", "Smith"),
    ("Jerry", "Smith"),
    ("Summer", "Smith"),
    ("Beth", "Smith"),
    ("Birdperson", ""),
    ("Squanchy", ""),
    ("", "Poopybutthole"),
    ("Revoli", "Clockberg Jr"),
]
names_df = spark.createDataFrame(data, schema)
names_df.show()

names_df.groupBy("lastname").count().show()



# wget -O adult.csv https://archive.ics.uci.edu/ml/machine-learning-databases/adult/adult.data

adultSchema = T.StructType([
    T.StructField("age", T.IntegerType()),
    T.StructField("workclass", T.StringType()),
    T.StructField("fnlwgt", T.FloatType()),
    T.StructField("education", T.StringType()),
    T.StructField("education-num", T.FloatType()),
    T.StructField("marital-status", T.StringType()),
    T.StructField("occupation", T.StringType()),
    T.StructField("relationship", T.StringType()),
    T.StructField("race", T.StringType()),
    T.StructField("sex", T.StringType()),
    T.StructField("capital-gain", T.FloatType()),
    T.StructField("capital-loss", T.FloatType()),
    T.StructField("hours-per-week", T.FloatType()),
    T.StructField("native-country", T.StringType()),
    T.StructField("income-class", T.StringType()),
])


adult_df = (
    spark.read
    .format("csv")
    .schema(adultSchema)
    .option("nullValue", " ?")
    .load("adult.csv")
)
adult_df.show()

adult_df.groupBy("income-class", "sex" ).agg({"hours-per-week": "mean"}).show()


flight_df = (
    spark.read
    .format("csv")
    .option("inferSchema", "true")
    .option("header", "true")
    .load("flights.csv")
)
# flight_df.show()

plane_df = (
    spark.read
    .format("csv")
    .option("inferSchema", "true")
    .option("header", "true")
    .load("plane-data.csv")
)
# plane_df.show()
tail_num = (
    plane_df
    .select("tailnum", "manufacturer")
    .where(F.col("manufacturer").isNotNull())
)
# tail_num.cache()

flight_manuf = (
    flight_df
    .select("AIRLINE", "TAIL_NUMBER")
    .join(tail_num, on=flight_df["TAIL_NUMBER"]==tail_num["tailnum"], how="inner")
)
# flight_manuf.show(20)


(
    flight_manuf
    .groupBy("AIRLINE", "manufacturer")
    .count()
    .sort(F.desc("AIRLINE"), F.desc("count"))
).show()


# SQL 
flight_df.createOrReplaceTempView("us_delay_flights_tbl")
spark.sql("""SELECT DISTANCE, ORIGIN_AIRPORT, DESTINATION_AIRPORT
FROM us_delay_flights_tbl WHERE DISTANCE > 1000
ORDER BY DISTANCE DESC
""").show(10)