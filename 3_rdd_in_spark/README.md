# Spark
Spark is an open-source software for distributed computing with emphasis on
- Data Science, 
- Machine Learning, 
- SQL analytics, 
- data streaming.

Distributed means capable of growing computational power with the number of machines involved. A group of machines connected with each other and running Spark constitute a cluster. Jobs are submitted to the dirver-node, while the driver controls all other subordinate nodes. In our case, we have only one node -- our computer. The good thing is -- the code written for a single Spark node can seamlessly be run on a cluster of nodes. Moreover, it will run faster.


# RDD
RDD - Resilient Distributed Dataset -  is the main abstraction of Spark. It represents a collection of elements partitioned across the nodes of a cluster.

We will not go in detail for all RDD operations. Just scratch the surface with `map`, `reduce`, `filter`. 

Let's have a look at the low-lever RDD interface in Spark.
```python
import pyspark

# as we know, spark is a separate software
# it has a bunch of interfaces to connect with
# we use a python package pyspark 
# that can transform our code into job instructions for spark
spark = (pyspark.sql.SparkSession.builder
         .appName("test_ml")
         .master("local[2]")
         .getOrCreate()
         )
sc = spark.sparkContext
```
```py
# ransform a list into RDD 
rdd_digits = sc.parallelize(
    [
        1, 2, 3, 4, 5, 6, 7, 8, 9, 0, 1, 2, 3, 4
    ]
)
```
```py
# increase each element by 1
rdd_digits_increment = (
    rdd_digits
    .map(lambda elem: elem + 1)
)
```
```py
# now guess what printing of RDD gives us
print(rdd_digits_increment)

# not much, the RDD object does not know exactly 
# what elements are in it.
# but if we want to find out, we call .collect() on the RDD
print(rdd_digits_increment.collect())

# RDD is an API to build spark jobs
# before a job is submitted an RDD object
# only keeps a track of requested transformations

# some methods of RDD object trigger 
# a job to be executed on spark -- so called actions
```

```py
# reduce operation gets the sum of values
sum_of_digits = (
    rdd_digits.reduce(lambda a, b: a + b)
    )
print(sum_of_digits)
```
Let's load a text file in RDD and count some words.  
At first, run in console 
```sh
wget https://www.gutenberg.org/files/2600/2600-0.txt
``` 
that will get us a .txt file.
```py
rdd_text = sc.textFile("2600-0.txt")
# get the top 10 most popular words in text
# 1) text in RDD looks like a list of lines
#    we use flatMap -- it applies function to each line
#    and merges the resulting collections (lists)
# 2) we make a pair out of each word (word, 1) 
#    to have a key and value to count
# 3) collect elements with the same first value in pair
#    and run a reduce operation on the second element in each group
#    that returns pairs (word, number_of_occurences)
# 4) we want only the top 10 most frequent words
#    for that in takeOrdered() we pass 10 as the number of top elements
#    and function that is used as a key for sorting
#    pair[1] means taking a second element of a pair
counts = (
    rdd_text
    .flatMap(lambda line: line.split(" "))      # 1
    .map(lambda word: (word, 1))                # 2 
    .reduceByKey(lambda a, b: a + b)            # 3
    .takeOrdered(10, lambda pair: - pair[1])    # 4
)
print(counts)
```

```py
# simmilar approach
# but now we count occurences of letters
# 1) for this we apply list() to the string
#    so it returns a list of letters
counts_letters = (
    rdd_text
    .flatMap(lambda line: list(line))          # 1
    .map(lambda letter: (letter, 1))
    .reduceByKey(lambda a, b: a + b)
    .takeOrdered(10, lambda pair: - pair[1])
)
print(counts_letters)
```

```py
# or we can count the number of lines 
# with word "pain" in those
count_pain = (
    rdd_text
    .filter(lambda line: "pain" in line)
    .count()
)
print(count_pain)
```

Many other operations over RDD are well documented in Spark API reference.
Those all follow the same `map` `reduce` logic. Transformations applied to elements have to be parallelizable, as much as possible. But there are cases when transformation of one element depends on other elements. 
> Transformnatin that depends only on one element is called ***narrow***.

> Transformation that depends on more than one elemen is called ***wide***.

Simple `map` or `flatMap` are narrow, `reduceByKey` is wide.

```py
# a good example of wide transformation 
# is sorting
# here we use a one-to-one function
# because RDD only has .sortBy() method,
# not .sort()
print(
    rdd_digits
    .sortBy(lambda x: x)
    .collect()
    )
```
---
---
# Tasks
## 1 Keep Triangles 
Given an array of numeric triplets `[(a, b, c), ...]` filter out only those that can build a triangle with corresponding side sizes.
You can build a triangle if `a + b >= c`.
Perform operation using Spark.

## 2 Distinct
Use PySpark documentation and write code that finds distinct values in RDD. 

## 3 CSV file
Try to load a comma separated file file into RDD, split each line by ",", and display top(10) rows.

> in console
```sh
# iris dataset from UCI 
# https://archive.ics.uci.edu/ml/datasets/iris
wget https://archive.ics.uci.edu/ml/machine-learning-databases/iris/bezdekIris.data 
```
> in python
```py
# as initial point
sc.textFile("bezdekIris.data")
```