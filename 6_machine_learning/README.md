# Spark ML

## Adult + Random Forest
We will use same UCI Adult datataset.
https://archive.ics.uci.edu/ml/datasets/adult

Last time we kept data files in the same folder as code.
Let's download those in a separate sub-folder.

```sh
mkdir data
wget https://archive.ics.uci.edu/ml/machine-learning-databases/adult/adult.data -P data
wget https://archive.ics.uci.edu/ml/machine-learning-databases/adult/adult.test -P data
```

```py
import pyspark
import pyspark.sql.functions as F
import pyspark.sql.types as T
from  pyspark.ml import Pipeline
from pyspark.ml.feature import StringIndexer, VectorAssembler
from pyspark.ml.classification import RandomForestClassifier


spark = (pyspark.sql.SparkSession.builder
         .appName("test_ml")
         .master("local[2]")
         .getOrCreate()
         )

# same commands to load adult dataset
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


df = (
    spark.read
    .format("csv")
    .schema(adultSchema)
    .option("nullValue", " ?")
    .load("data/adult.data")
)
# cache() command will tell Spark to keep the file in-memory
# to reduce reads from disk.
df.cache()
```
```py
# show the number of missing values per column 
df.select([F.count(F.when(F.col(col).isNull() | F.isnan(col), col)).alias(col) for col in df.columns]).show()
print("rows before drop", df.count())
# remove rows with missing values
df = df.na.drop()
# show the number of missing values per column after drop
df.select([F.count(F.when(F.col(col).isNull() | F.isnan(col), col)).alias(col) for col in df.columns]).show()
print("rows after drop", df.count())
# remove ative-country coulumn as it has
# too many categories for Random Forest
df = df.drop("native-country")
```
```py
# spark ML is mostly done with a Pipeleine abstraction
# Pipeline is assembled from Transformers applied consecutively


# StringIndexer is a Transformer that adds a column
# with string categories encoded into integers

# columns we need to encode
cat_cols = [
    "workclass", "education", "marital-status", "occupation", 
    "relationship", "race", "sex", "income-class"
]

# list of StringIndexers for each column
string_indexers = []
for col in cat_cols:
    stringIndexer = StringIndexer(inputCol=col, outputCol=f"{col}-indexed", handleInvalid="keep")
    string_indexers.append(stringIndexer)
```
```py
num_feats = ["age", "fnlwgt", "education-num", "capital-gain", "capital-loss", "hours-per-week"]
cat_feats = ["workclass", "education", "marital-status", "occupation", "relationship", "race", "sex"]
cat_feats_transformed = [f"{col}-indexed" for col in cat_feats]
inputCols = num_feats + cat_cols_transformed
# ML models in spark work only with an input numeric vector
# to collect several columns under one column of vectors
# use Transformer called VectorAssembler 
vectorAssembler = VectorAssembler(inputCols=inputCols, outputCol="features")
```
```py
# the last but not least
# Random Forest Transformer that will do classification
rf = RandomForestClassifier(featuresCol="features", labelCol="income-class-indexed")
```
```py
# list of all Transformers
stages = string_indexers + [vectorAssembler, rf]
# assembled Pipeline
model = Pipeline(stages=stages)
# to start using Pipeline we need to call fil() at first
# it fits each Transformer and trains Random Forest 
model = model.fit(df)
```
```py
# to run the prediction
# we call .transform over the fitted Pipeline
tdf = model.transform(df)
tdf.show()
# look throgh the columns that were added by our Pipeline
```
```py
# here is a traight-forward way to
# find model's accuracy on the train set
tdf.select(
    (
        F.count(F.when(F.col("prediction")==F.col("income-class-indexed"), "prediction")) / F.count("prediction")
    ).alias("acc")
).show()
```
```py
# now let's test the performance
# on the test set
# it is a bit broken, we need to 
# skip the first line
# here is a work-around with RDD
n_skip_rows = 1
row_rdd = (spark.sparkContext
    .textFile("data/adult.test")
    .zipWithIndex()
    .filter(lambda row: row[1] >= n_skip_rows)
    .map(lambda row: row[0])
)
df_test = (
    spark.read
    .schema(adultSchema)
    .option("nullValue", " ?")
    .csv(row_rdd)
)
```
```py
df_test = df_test.drop("native-country")
# the target label in the test set differs
# by dot [<=50K.] at the end
# remove it
df_test = df_test.withColumn("income-class", F.regexp_replace("income-class", r'\.', ""))
df_test.show(2)
```
```py
tdf = model.transform(df_test)

# accuracycon the test set
tdf.select(
    (F.count(F.when(F.col("prediction")==F.col("income-class-indexed"), "prediction")) / F.count("prediction")).alias("acc_test") 
).show()
```
---
---
# Task
## 1 Still Adult
Try to apply any other classifier from Spark ML for the same setup.
## 2 Roses are red, Iris is f(x, y, z, t)
Train a Decision Tree classifier for Iris dataset https://archive.ics.uci.edu/ml/datasets/iris (https://archive.ics.uci.edu/ml/machine-learning-databases/iris/iris.data)

Make a train and test split for data. You will need `sampleBy` and `substract` methods of DataFrame. Choose the Tartsformers needed.
