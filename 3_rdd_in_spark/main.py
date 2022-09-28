import pyspark

spark = (pyspark.sql.SparkSession.builder
         .appName("test_ml")
         .master("local[2]")
         .getOrCreate()
         )
sc = spark.sparkContext


rdd_digits = sc.parallelize(
    [
        1, 2, 3, 4, 5, 6, 7, 8, 9, 0, 1, 2, 3, 4
    ]
)

print(rdd_digits.sortBy(lambda x: x).collect())
# print(rdd_digits)

rdd_digits_increment = (
    rdd_digits
    .map(lambda elem: elem + 1)
)

print(rdd_digits_increment)
print(rdd_digits_increment.collect())

sum_of_digits = (
    rdd_digits.reduce(lambda a, b: a + b)
    )
print(sum_of_digits)


# download a txt file
# in a console run 
# wget https://www.gutenberg.org/files/2600/2600-0.txt
rdd_text = sc.textFile("2600-0.txt")
counts = (
    rdd_text
    .flatMap(lambda line: line.split(" "))
    .map(lambda word: (word, 1))
    .reduceByKey(lambda a, b: a + b)
    .takeOrdered(10, lambda pair: - pair[1])
)


counts_letters = (
    rdd_text
    .flatMap(lambda line: list(line))
    .map(lambda letter: (letter, 1))
    .reduceByKey(lambda a, b: a + b)
    .takeOrdered(10, lambda pair: - pair[1])
)


count_pain = (
    rdd_text
    .filter(lambda line: "pain" in line)
    .count()
)


arr = [(1, 2, 3), (4, 5, 6), (7, 8, 9), (10, 11, 12)]

rdd_tripplets = sc.parallelize(arr)
min_vals = (
    rdd_tripplets
    .map(lambda triplet: min(triplet))
    .collect()
)
print(min_vals)