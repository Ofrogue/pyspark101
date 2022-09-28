# Structured Streaming

Good thing about structures streaming in Spark is that it supports same interface as DataFrames.

Download a file with stock orders

```sh
wget -O orders.tar.gz https://github.com/spark-in-action/first-edition/blob/master/ch06/orders.tar.gz?raw=true

tar -xf orders.tar.gz
```

Split the downloaded file into smaller files. We will use those to emulate a stream behavior.
```sh
sh split.sh orders.txt
```

```py
import pyspark
import pyspark.sql.functions as F
import pyspark.sql.types as T


spark = (pyspark.sql.SparkSession.builder
         .appName("test_streaming")
         .master("local[2]")
         .getOrCreate()
         )
```
```py
schema = T.StructType([
    T.StructField("date", T.StringType()),
    T.StructField("index", T.IntegerType()),
    T.StructField("userid", T.IntegerType()),
    T.StructField("stock_code", T.StringType()),
    T.StructField("amount", T.IntegerType()),
    T.StructField("price", T.FloatType()),
    T.StructField("buy_sell", T.StringType())
])

# stream reading is simmilar to simple reading from some source 
# 3) only one file will be processed at a time
#    without this parameter spark will process all files
#    in a folder in one batch
dataStream = (
    spark.readStream
    .format("csv") #  1
    .schema(schema) #  2 
    .option("maxFilesPerTrigger", 1) #  3 
    .load("orders_cache/") #  4
)
```
```py
# transformation instruction
# keep amount of buying positions per stock
count = (
    dataStream
    .filter(F.col("buy_sell")=="B")
    .groupBy(["stock_code"]).agg({"amount": "sum"})
    )
```
```py
# initiate stream into console (for demonstration purposes)
# 1) console format is used only for debugging
# 2) keep the track of previous records
#    consult documentation for other output modes
#    https://spark.apache.org/docs/latest/structured-streaming-programming-guide.html
# 3) initiate
# 4) terminate on keyboard interrupt
(
    count.writeStream
    .format("console") #  1
    .outputMode("complete") #  2
    .start() #  3
    .awaitTermination() #  4
)
```
---
---
# Task
Try to count the traded cumulative price of stocks bought. `amount` * `price` sum per stock.