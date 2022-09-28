import pyspark
import pyspark.sql.functions as F
import pyspark.sql.types as T


spark = (pyspark.sql.SparkSession.builder
         .appName("test_streaming")
         .master("local[2]")
         .getOrCreate()
         )


# https://github.com/spark-in-action/first-edition/blob/master/ch06/orders.tar.gz
userSchema = T.StructType([
    T.StructField("date", T.StringType()),
    T.StructField("index", T.IntegerType()),
    T.StructField("userid", T.IntegerType()),
    T.StructField("stock_code", T.StringType()),
    T.StructField("amount", T.IntegerType()),
    T.StructField("price", T.FloatType()),
    T.StructField("buy_sell", T.StringType())
])

dataStream = (
    spark.readStream
    .format("csv")
    .schema(userSchema) 
    .option("maxFilesPerTrigger", 1)
    .load("orders_cache/")   
)

count = (
    dataStream
    .filter(F.col("buy_sell")=="B")
    .groupBy(["stock_code"]).agg({"amount": "sum"})
    )

(count.writeStream
.format("console")
.outputMode("complete")
.start()
.awaitTermination()
)