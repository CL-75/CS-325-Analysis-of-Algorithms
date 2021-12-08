# Casey Levy
# CS 325 - HW 2 - stoogeSort.py
# Implementing stooge sort method given from HW 2 to sort an array and writing
#   the data to an output file

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

    with open('data.txt', 'r') as file:
        for line in file:
            new = (line.strip().split())
            sort = [int(i) for i in new[1:]]
            size = len(sort) - 1
            stoogeSort(sort, 0, size)

            with open('stooge.out', "a") as out:
                out.write(' '.join(str(i) for i in sort))
                out.write("\n")


if __name__ == "__main__":
    main()

