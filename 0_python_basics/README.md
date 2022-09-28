# Python !

Python is a programming language :)
```python
print("hello world")
```
> Here and after we encourage you to use `print` at any possible occasion. In python you can pass into `print()` almost anything and gain some unrestanding of what that is.
# Functions
```python
# you can write your function with a key-word def
# here we define a function called echo that prints whatever we pass into it
def echo(value):
    print(value)
```
```python
# to call your function use parentheses
echo(100)
echo("hi")
echo([1,2,3])
```
```python
echo()
# whoops! that should give us a TypeError
# the funcion does not know what to do with no arguments
```
```python
# but, if we want it to print something anyway
# we can use a default value notation
def echo(value="no argument passed"):
    print(value)

echo(100)
echo("hi")
echo([1,2,3])
echo()

# once the function is called without its argument specified, it uses a default value
```

```python
# you can build functions that take any number of arguments
# say, two arguments
def sum_two(a, b):
    return a + b
# here we used a return statement 
# return x means that the function has to return that value

# the returned value can be assigned to a variable
returned_value = sum_two(100, 10)

# or passed to another function
print(sum_two(100, 10))

print(sum_two("Strings", " can be added"))

print(sum_two("string", 100))
# Python does not know how to add strings and integers together
# we get a TypeError
```

# Types
By this time you may have noticed that Python is not a strongly typed language as, say, Java. It is dynamically typed!
```python
# try this, type() is a built-in to check types
clock = 10
print(type(clock))
clock = "ten"
print(type(clock))
# type of the variable is updated with the variable
```
Python supports typing, and it is used in a bigger projects, but for it is not strictly necessary.
```python
# other usefull type is bool
# it can be either True or Flase
print(2 > 1)
print(2 < 1)
print(1 == 1)
```
```python
# None is a separate type 
# it is used to describe the absence of a value

# any function always returns something 
# if there is no explicit return statement,
# it returnes None

# let's try it with built-in function print()
print_returned = print()
# and now let's print the result
print(print_returned)
```

# Lists and Dicts
There are useful built-in data structures in Python that help a lot during programming. These are `list` and `dict`. 
## List
```python
# you can think about list as about array of values
# list can be defined with square parentheses
list_1 = [1, 2, 3, 4]

empty_list = []

# list can contain values of different types
list_2 = [1, 2, "three"]

# list can be indexed with square parentheses starting from index 0

print(list_2[0])
print(list_2[1])

# as well list supports negative indexes
print(list_2[-1])
# -1 means the last element,
print(list_2[-2])
# -2 means the second element from the end


# list also supports slicing 
# to get a slice of the first 2 elements
print(list_2[:2])

# to get a slice of all elements after the first two
print(list_2[2:])

# to get the slice of elemnts between the first and the last element
print(list_2[1:-1])
```
```python
# list is a modifiable type
arr = [1, 2, 3]
# you can add a value in the end
arr.append(10)
print(arr)

# and remove the value as well
arr.pop()
print(arr)
```

## Dict
```python
# dict is a collection of key-value pairs 
# defined with curly brackets
# with {key: value} syntax 
dict_0 = {"one": 1, "two": 2, "three": 3}

empty_dict = {}

# dict is subscriptable (square parentheses can be applied) like list
# but with the key
print(dict_0["one"])
```
```python
# you can try to get an unexistent key
print(dict_0["zero"])
# KeyError exception should be thrown
```
```python
# if you are not sure if the key is in the dict
# you can use a .get(key) method
print(dict_0.get("one"))
print(dict_0.get("zero"))
# the .get method returns None by default if does not 
# find a corresponding key in the dict

# instead of None you can make .get() method to return whatever you 
# want on missing key: just put a second positional argument 
print(dict_0.get("zero", "MISSING_VALUE"))
```

## Tuple
```python
# tuple is pretty much the same thing as a list, but immutable
# defined with parenthesis
tuple_1 = (1, 2, "dog")
```
```py
# due to immutability tuple can be used as a key in dict
# imagine keeping Tic-Tac-Toe game in a dict using 2 coordinates
game = {
    (0, 0): "X", 
    (0, 1): "X",
    (0, 2): "O",
    (1, 1): "",
    (1, 1): "",
    (1, 2): "",
    (2, 0): "O",
    (2, 1): "O",
    (2, 2): "X",
} 
```

# Loops
What a programming language without loops! 
```python
# simple for loop is done over an iterable object
# say, list
arr = [1, 3, 2, 4, 5, 6, 7, 8, 8, 9]
for val in arr:
    print(val + 10)
```
```python
# sometimes we need to iterate over integers up to N
# for that we use a built-in generator range()
for i in range(10):
    print(">>", i)
```

```python
# you can do equivalent loop with while keyword
i = 0
while i < 10:
    print(">>", i)
    i = i + 1
# while is less common in simple loops as it is more verbose
```

```python
# say, we want to add elements in the list within the loop
# .append() is a method of a list that allows to add an element in it 
arr = []
for i in range(10):
    arr.append(i)

print(arr)
```
# Conditional Statements
```python
# python has a conditional statement if
value = 10
if value > 10:
    print("greater than 10")
else:
    print("smaller than 10 or equal to 10")
```
```py
# let's build a function that prints if a value is greater than 10
def greater_10(value):
    if value > 10:
        print(value, "is greater than 10")
    else:
        print(value, "is smaller than 10 or equal to 10")

greater_10(20)
```
```py
# we can also call greater_10 in a loop
for i in range(20):
     greater_10(i)
```
```py
# if statement does not necessarily have to be followed by else
# the code inside the if statement will be ran only if the testerd condition is True

# let's add to the list only even numbers from 0 to N
def list_even_numbers(n):
    res = []
    for i in range(n):
        if i % 2 == 0:
            res.append(i)

    return res

print(list_even_numbers(15))
```

# Variable Unpackig
```python
# in python you can assing variables in a funny way
a, b = 10, 5

# in a nutshell, it is assignment of tuples
(a, b) = (10, 5)
```
```py
# that is handy when we want to loop over two lists simultaneously 

arr_1 = [1, 2, 3]
arr_2 = ["a", "b", "c"]
# for that we use built-in zip()
for number, letter in zip(arr_1, arr_2):
    print(number, letter)
```
```py
# if we need to track an index of an element
# enumerate() built-in is helpfull
for i, letter in enumerate(arr_2):
    print(letter, "has index", i)
```

# Comprehensions
```python
# ususally writing a whole for loop to modify a list might be too verbose
# python has list comprehensions --
# a syntactic sugar to make code look better in some cases 

# say, we a have a list of file names in a folder
# and we want to make a list paths to that files

file_list = ["file01.txt", "file12.txt", "file13.txt"] 
folder_name = "new_folder"
file_paths = [folder_name + "/" + file for file in file_list]
print(file_paths)
```

```python
# if statetment can also be added
# to keep only even numbers in a list
arr = [1, 2, 3, 4, 5, 6, 7, 8]
even_arr = [elem for elem in arr if elem % 2 == 0]
print(even_arr)
```
# Strings
Last but not least. Python is very handy for string manipulation out-of-the-box.
```py
# string is immutable object
# you can not modify it as list
# but you can acccess it by index
date = "01.09.2022"
print(date[0])
# and slice as well
print(date[-4:])
```
```py
# strings can be added to return a new 
# concatenated string
foo = "foo"
bar = "bar"
new_string = foo + bar
print(new_string)
```
```py
# strings can be splitted by whitespace
string = "one two three"
string_list = string.split()
print(string_list)

# symbol to split by can be arbitrary
string = "one, two, three"
string_list = string.split(", ")
print(string_list)
```
```py
# the resulting list can be joined back to string
new_string = "*".join(string_list)
print(new_string)
new_string = "|".join(string_list)
print(new_string)
```
```py
# strings in python support formatting
value = 2**100
print(f"2 to the power of 100 is {value}")

# as well you can use .format() method
print(
    "{} loves {} and hates {}".format("CAT", "BEEF", "VACUUM CLEANER")
)
```
---
---
# Tasks
## 1 Sort
Google how to sort a list in Python and create a function that takes a list and returnes a sorted a list.

## 2 Mean
Create a function that returns an average of numeric list values

## 3 Median
Create a function that returns a median value of the elements in the paased list.
##  4 Count
Create a  list in Python and create a function that sorts a list 
function that takes a list and counts how many times each value appears in that list. The function should return a `dict` with `value: number` pairs.
