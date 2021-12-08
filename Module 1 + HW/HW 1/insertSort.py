# Casey Levy
# CS 325 - HW 1 - insertsort.py
# Creating a insertsort program to sort an array of integers in ascending order

def insertsort(array):
    size = len(array)

    # Traversing the array
    for x in range(1, size):
        key = array[x]
        y = x - 1

    # Moving integers into their proper place through value comparison
    # Some code cited from course textbook, Introduction to Algorithms by Cormen, Leiserson, Rivest, and Stein
    #   page 18
        while y >= 0 and array[y] > key:
            array[y + 1] = array[y]
            y -= 1
        array[y + 1] = key


# Method to read file and output data to merge.txt
def read_file(fileName):
    merged = ''        # New string
    for data_line in open(fileName):
        data = data_line.split()       # Ignoring first number on each line
        data_ints = [int(i) for i in data[1:]]        # Converting strings to ints

        insertsort(data_ints)    # Calling mergesort to sort integers
        data_ints = [str(j) for j in data_ints]     # Converting ints to strings
        merged += ' '.join(data_ints) + "\n"

    a = open('insert.out', 'w')
    a.write(merged)
    a.close()

read_file('data.txt')
