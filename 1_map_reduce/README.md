# Map, Reduce and a teaspoon of Functional programming
I this practical session we will learn 
`map`, `reduce` and `filter` operatios that originate from functional programming paradigm.
## Background

Functional programming is the paradigm to build a computation as composition of functions.
>Composition of two functions $f$ and $g$ is defined as follows $f \circ g \equiv f(g())$. 

Function plays a role of a parameter of another function.  
In the pure functional programming everything is a function or a constant. The functions are not dependant on anything except their parameters and don't modify any parameters, so called pure functions. Even constants are defined as functions. 

Most of the existing software is written as a line of consecutive instructions that have to be executed one by one with the strictly defined order. That worked well for years starting from the dawn of computers. But such an approach is designed for and limited by the speed of the sigle CPU core. A single core speed does not grow as fast today as it was in the 90's. The humanity is left with no choice except growing a computation power by increasing the amout of CPU cores. But a single core programming approach is usually difficult or sometimes impossibe to port on multiple cores efficiently. 

To run code faster we need to parallelize it. To parallelize -- we need to split it into not interacting with each other chunks. The functions that depend only on the parameters (pure) are fairly compliant to be such chunks. 
It leads us to a simple conclusion: pure functions help to run code faster on a multi-core CPU. 

## Python
Python is a multi-paradigme language, so some useful elements of functional programming can be explored with it.
### Map
```python
# let's define a function that returns a value incremented by 1  
def incement(x):
    return x + 1

# and a simple list we want to modify
arr = [1, 2, 3, 4, 5]


# how do we modify each element with python?
arr2 = [increment(elem) for elem in arr]


# but, there is a way to do the same thing with map
# map takes a function as a first argument and iterable object as a second argument
# to observe the result we transform it to list
arr3 = list(
    map(
        increment,
        arr
    )
)


# defining a separate function for just adding 1 is not handy
# there is another way to define such functions with the lambda keyword

arr4 = list(
    map(
        lambda x: x+1,
        arr
    )
)


# input parameters defined before semicolon and the transformation after semicolon
add_two = lambda x, y: x + y
# is equivalent to
def add_two(x, y):
    return x + y
```

### Filter
```python
# we also modify lists by filtering out some or the elements
# pythonic way to do it is
arr = [1, 2, 3, 4, 5, 6]
arr2 = [elem for elem in arr if elem > 4]


# to do it in a functional way ...
# filter takes two positional arguments: function that return True or False,
# and iterable
arr3 = list(
    filter(
        lambda x: x > 4,
        arr
    )
)
```
### Reduce
```python
from functools import reduce

arr = [1, 2, 3, 4, 5, 6]

# reduce takes 3 arguments
# reduce(function, iterable, initializer)
arr_sum = reduce(
    lambda x, y: x + y,
    arr,
    0
)
# is equivalent to 
arr_sum = ((((((0 + 1)+ 2) + 3) + 4) + 5) + 6)
# where initializer == 0


# reduce can also take only 2 arguments
# reduce(function, iterable)
# then
arr_sum = reduce(
    lambda x, y: x + y,
    arr
)
# is equivalent to 
arr_sum = (((((1 + 2) + 3) + 4) + 5) + 6)
```

## Example
Count for each triplet the smallest value using `map` and `reduce`?
```python
arr = [(1, 2, 3), (4, 5, 6), (7, 8, 9), (10, 11, 12)]

res = list(
    map(
        lambda triplet: min(triplet),
        arr
    )
)


# res is already a result we need, but we used a built-in function min()
# let's create a function to find minimum with reduce
def min_reduce(iterable):
    return (
        reduce(
            lambda x, y: x if x < y else y,
            iterable,
            float("inf")
        )
    )

# and now we can rewrite our code only using map and reduce
res = list(
    map(
        lambda triplet: min_reduce(triplet),
        arr
    )
)
```
---
---
# Tasks
## 1 FizzBuzz
Create a function that takes an integer N and creates a list of integers 1 to N, but substitutes element with “Fizz” if an integer is divisible by 3, “Buzz” if an integer is divisible by 5, and “FizzBuzz” if an integer is divisible by both 3 and 5 using `map`.
Note that you can use python one line conditional operator
```python
a = 1
b = 2

d = max(a, b)
# is eqivalent to
d = lambda a, b: a if a > b else b
```
but as well you can use a regular function instead of lambda expression.


## 2. Sum of Odd
Create a function that takes an iterable as an argument and returns a sum of odd numbers in it using `map`, `filter` and `reduce`.