def echo(value="no value"):
    print(value)


echo(100)
echo("hi")
echo([1,2,3])

echo()


def sum_two(a, b):
    return a + b

print(sum_two(100, 10))

print(sum_two("Strings", " can be added"))

# print(sum_two("string", 100))


def add_two_int(a: int, b: int) -> int:
    return a + b

print(add_two_int("hi", "mom"))

print(type(10))

print(type(""))


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


# dict is a collection of key-value pairs 
# defined with curly brackets
# with {key: value} syntax 
dict_0 = {"one": 1, "two": 2, "three": 3}

empty_dict = {}

# dict is subscriptable (square parentheses can be applied) like list
# but with the key
print(dict_0["one"])

# you can try to get an unexistent key
# print(dict_0["zero"])
# KeyError should be thrown by python


# if you are not sure if the key is in the dict
# you can use a .get(key) method
print(dict_0.get("one"))
print(dict_0.get("zero"))


list_2.append(12)


file_list = ["file01.txt", "file12.txt", "file13.txt"] 
folder_name = "new_folder"
file_paths = [folder_name + "/" + file for file in file_list]
print(file_paths)

arr = [1, 2, 3, 4, 5, 6, 7, 8]
even_arr = [elem for elem in arr if elem % 2 == 0]
print(even_arr)