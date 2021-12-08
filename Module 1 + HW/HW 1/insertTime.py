


import random, time

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


# Recording runtime for arrays of size n
def main():


    array = [5000, 6000, 7000, 8000, 9000, 10000, 11000]
    for i in range(len(array)):
        new_arr = []

        for j in range(array[i]):
            new_arr.append(random.randint(-10000, 10000))

        begin = time.process_time()
        insertsort(new_arr)
        end = time.process_time()
        print("\nSize of array (n): ", len(new_arr))
        print("Time Elapsed (in seconds): ", end - begin)



if __name__ == "__main__":
    main()