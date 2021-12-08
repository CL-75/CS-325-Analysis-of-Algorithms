# Casey Levy
# CS 325 - HW 2 - stoogeTime.py
# Implementing stooge sort method given from HW 2 to sort arrays of various lengths
#   and also timing how long it takes to complete.

import random, time

# Code inspired from https://www.geeksforgeeks.org/stooge-sort/
def stoogeSort(arr, l, r):
    if l >= r:
        return

    if arr[l] > arr[r]:
        x = arr[l]
        arr[l] = arr[r]
        arr[r] = x

    if r-l + 1 > 2:
        y = (int)((r-l + 1)/3)
        stoogeSort(arr,  l, (r-y))
        stoogeSort(arr, l+y, (r))
        stoogeSort(arr, l, (r-y))

def main():

    n = [300, 600, 900, 1200, 1500, 1800, 2100]

    n_size = len(n)
    count = 0

    while count < n_size:
        array = [random.randint(0, 5000) for i in range(n[count])]
        size = len(array) - 1
        begin = time.time()

        stoogeSort(array, 0, size)

        end = time.time()
        print("\nSize of array (n): ", str(n[count]))
        print("Time Elapsed (in seconds): ", end - begin)
        count += 1


if __name__ == "__main__":
    main()