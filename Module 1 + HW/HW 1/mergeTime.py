# Casey Levy
# CS 325 - HW 1 - mergeTime.py
# Creating a mergesort program to sort an and generate an array of random integer values

import random, time

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

# Recording runtime for arrays of size n
def main():


    array = [120000, 140000, 160000, 180000, 200000, 220000, 240000]
    for i in range(len(array)):
        new_arr = []

        for j in range(array[i]):
            new_arr.append(random.randint(-10000, 10000))

        begin = time.process_time()
        mergesort(new_arr)
        end = time.process_time()
        print("\nSize of array (n): ", len(new_arr))
        print("Time Elapsed (in seconds): ", end - begin)



if __name__ == "__main__":
    main()

