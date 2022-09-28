# adult dataset
# https://archive.ics.uci.edu/ml/datasets/adult


# mkdir data
# wget https://archive.ics.uci.edu/ml/machine-learning-databases/adult/adult.data -P data
# wget https://archive.ics.uci.edu/ml/machine-learning-databases/adult/adult.test -P data


# age: continuous.
# workclass: Private, Self-emp-not-inc, Self-emp-inc, Federal-gov, Local-gov, State-gov, Without-pay, Never-worked.
# fnlwgt: continuous.
# education: Bachelors, Some-college, 11th, HS-grad, Prof-school, Assoc-acdm, Assoc-voc, 9th, 7th-8th, 12th, Masters, 1st-4th, 10th, Doctorate, 5th-6th, Preschool.
# education-num: continuous.
# marital-status: Married-civ-spouse, Divorced, Never-married, Separated, Widowed, Married-spouse-absent, Married-AF-spouse.
# occupation: Tech-support, Craft-repair, Other-service, Sales, Exec-managerial, Prof-specialty, Handlers-cleaners, Machine-op-inspct, Adm-clerical, Farming-fishing, Transport-moving, Priv-house-serv, Protective-serv, Armed-Forces.
# relationship: Wife, Own-child, Husband, Not-in-family, Other-relative, Unmarried.
# race: White, Asian-Pac-Islander, Amer-Indian-Eskimo, Other, Black.
# sex: Female, Male.
# capital-gain: continuous.
# capital-loss: continuous.
# hours-per-week: continuous.
# native-country: United-States, Cambodia, England, Puerto-Rico, Canada, Germany, Outlying-US(Guam-USVI-etc), India, Japan, Greece, South, China, Cuba, Iran, Honduras, Philippines, Italy, Poland, Jamaica, Vietnam, Mexico, Portugal, Ireland, France, Dominican-Republic, Laos, Ecuador, Taiwan, Haiti, Columbia, Hungary, Guatemala, Nicaragua, Scotland, Thailand, Yugoslavia, El-Salvador, Trinadad&Tobago, Peru, Hong, Holand-Netherlands.

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


adultSchema = T.StructType([
    T.StructField("age", T.IntegerType()),
    T.StructField("workclass", T.StringType()),
    T.StructField("fnlwgt", T.FloatType()),
    T.StructField("education", T.StringType()),
    T.StructField("education-num", T.FloatType(), True),
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
df.cache()

# df.select([F.count(F.when(F.col(col).isNull() | F.isnan(col), col)).alias(col) for col in df.columns]).show()
# print("rows before drop", df.count())
df = df.na.drop()
# df.select([F.count(F.when(F.col(col).isNull() | F.isnan(col), col)).alias(col) for col in df.columns]).show()
# print("rows after drop", df.count())
df = df.drop("native-country")


cat_cols = [
    "workclass", "education", "marital-status", "occupation", "relationship", "race", "sex",
    #  "native-country",
    "income-class"
]
string_indexers = []
for col in cat_cols:
    stringIndexer = StringIndexer(inputCol=col, outputCol=f"{col}-indexed", handleInvalid="keep")
    string_indexers.append(stringIndexer)


num_feats = ["age", "fnlwgt", "education-num", "capital-gain", "capital-loss", "hours-per-week"]
cat_cols_no_target = cat_cols[:-1]
cat_cols_transformed = [f"{col}-indexed" for col in cat_cols_no_target]
inputCols = num_feats + cat_cols_transformed
vectorAssembler = VectorAssembler(inputCols=inputCols, outputCol="features")


rf = RandomForestClassifier(featuresCol="features", labelCol="income-class-indexed")


stages = string_indexers + [vectorAssembler, rf]
model = Pipeline(stages=stages)
model = model.fit(df)
tdf = model.transform(df)
tdf.show(20)
print(tdf.count())
tdf.select(
    (
        F.count(F.when(F.col("prediction")==F.col("income-class-indexed"), "prediction")) / F.count("prediction")
    ).alias("acc")
).show()

# to check labels
# model.stages[0].labels

n_skip_rows = 1
row_rdd = (spark.sparkContext
    .textFile("data/adult.test")
    .zipWithIndex()
    .filter(lambda row: row[1] >= n_skip_rows)
    .map(lambda row: row[0])
)
df_test = spark.read.schema(adultSchema).option("nullValue", " ?").csv(row_rdd)



# df_test = df_test.na.drop()
df_test = df_test.drop("native-country")
# df_test = df_test.withColumn("income-class", F.when(F.col("income-class")==" <=50K.", F.lit(" <=50K")).otherwise(F.lit(" >50K")))
df_test = df_test.withColumn("income-class", F.regexp_replace("income-class", r'\.', ""))
# df_test.show()
tdf = model.transform(df_test)
# tdf.show(20)
print(tdf.count())
tdf.select(
    (F.count(F.when(F.col("prediction")==F.col("income-class-indexed"), "prediction")) / F.count("prediction")).alias("acc_test") 
).show()
