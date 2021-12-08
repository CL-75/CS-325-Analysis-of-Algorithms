# Casey Levy
# CS 325 - HW 1 - mergesort.py
# Creating a mergesort program to sort an array of integers in ascending order
#   by using Divide and Conquer method

def mergesort(array):
    size = len(array)

    if size > 1:
        mid = size // 2        # Finding middle of array by dividing by 2
        left = array[:mid]     # Setting array elements into 2 halves for sorting purposes
        right = array[mid:]
        mergesort(left)        # Recursion to sort each half
        mergesort(right)

        # Creating temp arrays and copying data into them
        x, y, z = 0, 0, 0
        left_half = len(left)
        right_half = len(right)

        # Traversing each half and adding integers to array
        # Some lines cited from https://www.askpython.com/python/examples/merge-sort-in-python
        while x < left_half and y < right_half:
            if left[x] < right[y]:
                array[z] = left[x]
                x += 1

            else:
                array[z] = right[y]
                y += 1
            z += 1

        # Must account for uneven lists/odd valued halves
        while x < left_half:
            array[z] = left[x]
            x += 1
            z += 1

        while y < right_half:
            array[z] = right[y]
            y += 1
            z += 1


# Method to read file and output data to merge.txt
def read_file(fileName):
    merged = ''        # New string
    for data_line in open(fileName):
        data = data_line.split()       # Ignoring first number on each line
        data_ints = [int(i) for i in data[1:]]        # Converting strings to ints

        mergesort(data_ints)    # Calling mergesort to sort integers
        data_ints = [str(j) for j in data_ints]     # Converting ints to strings
        merged += ' '.join(data_ints) + "\n"

    a = open('merge.out', 'w')
    a.write(merged)
    a.close()

read_file('data.txt')

