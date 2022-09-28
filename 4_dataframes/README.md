# DataFrames (1/2)

Good tutorial about DataFrames in Spark
https://towardsdatascience.com/the-most-complete-guide-to-pyspark-dataframes-2702c343b2e8


DataFrames are a handy abstraction that can be regarded as spreadsheet tables.
Similar data structure with the same name can be found in R and  `pandas` Python.
DaraFrame has columns, and each column has a specific type -- same as in relational databases.

## Let's create a DtaFrame from scratch!
```py
import pyspark
import pyspark.sql.functions as F
import pyspark.sql.types as T


spark = (pyspark.sql.SparkSession.builder
         .appName("test_df")
         .master("local[2]")
         .getOrCreate()
         )


# python list of tuples
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

# schema to describe columns
schema = T.StructType([
    T.StructField("firstname", T.StringType()),
    T.StructField("lastname", T.StringType())
])

# assemble our dataframe
names_df = spark.createDataFrame(data, schema)
names_df.show()
```
```py
# similar to R or pandas in python
# dataframes in spark have a rich API for tranformations

# Number of rows with the same lastname
(
    names_df
    .groupBy("lastname")
    .count()
    .show()
)
```
```py
# schema definition might look too verbose
# but it gives more control
schema = T.StructType([
    T.StructField("firstname", T.StringType(), True),
    T.StructField("lastname", T.StringType(), True)
])

# there is an other way to define schema
# with SQL notation
schema = "firstname STRING, lastname STRING"
names_df = spark.createDataFrame(data, schema)
names_df.show()

# for more SQL notation types consult with documentation
# https://docs.databricks.com/spark/latest/spark-sql/language-manual/sql-ref-datatypes.html
```

## Loading from file
At first, in a console download the comma separated file
```sh
wget -O adult.csv https://archive.ics.uci.edu/ml/machine-learning-databases/adult/adult.data

```
You can read about this dataset at https://archive.ics.uci.edu/ml/datasets/adult
```py
# structure for this dataset is massive
# 15 columns
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

# to read the file into dataframe
# we need to specify 
# 1) format
# 2) schema
# 3) any other options
#    here we explicitly define the missing value sign 
# 4) path to the file
adult_df = (
    spark.read
    .format("csv")  #  1
    .schema(adultSchema) #  2
    .option("nullValue", " ?") #  3
    .load("adult.csv") #  4
)
adult_df.show()
```
```py
# data analysis can be held within spark dataframes
(
    adult_df
    .groupBy("income-class", "sex" )
    .agg({"hours-per-week": "mean"})
    .show()
)
```
---
---
## Task
Find the average, min and max of `education-num` per other column of your choice.

---

# ///////////////////////////////////////////

---

# DataFrames (2/2)
```py
import pyspark
import pyspark.sql.functions as F
import pyspark.sql.types as T


spark = (pyspark.sql.SparkSession.builder
         .appName("test_df")
         .master("local[4]")
         .getOrCreate()
         )
```
## The most popular aircraft producer
We will use the dataset of flight delays in the US 2015.
https://www.kaggle.com/datasets/usdot/flight-delays?select=flights.csv

Download two files in a console
```sh
wget -O flights.csv https://figshare.com/ndownloader/files/17614757
```
```sh
wget -O plane-data.csv https://raw.githubusercontent.com/neo4j-contrib/training/master/modeling/data/aircraft.csv
```

```py
# csv files can have headers
# spark dataframes are capable of infering 
# schema from a file header and content
flight_df = (
    spark.read
    .format("csv")
    .option("inferSchema", "true")
    .option("header", "true")
    .load("flights.csv")
)
# flight_df contains data about the US flights in 2015 including delays
flight_df.show()
```
```py
plane_df = (
    spark.read
    .format("csv")
    .option("inferSchema", "true")
    .option("header", "true")
    .load("plane-data.csv")
)
# plane_df is the registry information about planes 
plane_df.show()
```
```py
# plane_df has many missing values
# we can filter those out
# and keep only manufacturer information
tail_num = (
    plane_df
    .select("tailnum", "manufacturer")
    .where(F.col("manufacturer").isNotNull())
)
tail_num.show()
```
```py
# JOIN operation is available in spark
# we have flights in one table
# and manufacturer in another table
# those can be joined on TAIL_NUMBER key
flight_manuf = (
    flight_df
    .select("AIRLINE", "TAIL_NUMBER")
    .join(tail_num, on=flight_df["TAIL_NUMBER"]==tail_num["tailnum"], how="inner")
)
flight_manuf.show(20)
```
```py
manuf_by_airline = (
    flight_manuf
    .groupBy("AIRLINE", "manufacturer")
    .count()
)
manuf_by_airline.show()
# the airlines are not grouped 
```
```py
manuf_by_airline = (
    flight_manuf
    .groupBy("AIRLINE", "manufacturer")
    .count()
    .sort(F.desc("AIRLINE"), F.desc("count"))  #  to keep airlines sorted togehter use .sort
)
manuf_by_airline.show()
```

## SQL
```py 
# transformations over dataframes can be done with SQL

# create a table name reference for SQL 
flight_df.createOrReplaceTempView("us_delay_flights_tbl")

# show longest distance flights
spark.sql("""SELECT DISTANCE, ORIGIN_AIRPORT, DESTINATION_AIRPORT
FROM us_delay_flights_tbl WHERE DISTANCE > 1000
ORDER BY DISTANCE DESC
""").show(10)
```
---
---

# Task
## Park, my park
Previous transformations tell which manufacturer is most frequently used by company.
Can you propose how to count the distribution of unique aircrafts per airline company? Use search engine of your choice and Spark DataFrames documentation.
## Back to Chicago
What is the most popular destination airport (DESTINATION_AIRPORT) on Mondays?
In the US they start weeks from Sunday.