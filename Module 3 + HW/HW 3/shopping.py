# Casey Levy
# CS 325 - HW 3 - Problem 4
# Creating a program that determines the max total price of items each family
#   should select after they've won a shopping spree

# Code inspired from www.geeksforgeeks.org/0-1-knapsack-problem-dp-10/

def shoppingSpree(weight, vals, W, n):
    if n == 0 or W == 0:
        return 0

    A = [[0 for x in range(W+1)] for i in range(n+1)]

    for i in range(n+1):
        for x in range(W+1):
            if i == 0 or x == 0:
                A[i][x] = 0

            elif weight[i-1] <= x:
                A[i][x] = max(vals[i-1] + A[i-1][x-weight[i-1]], A[i-1][x])

            else:
                A[i][x] = A[i-1][x]

    res = A[n][W]
    result = res
    x, items = W, []
    for i in range(n, 0, -1):
        if result <= 0:
            break

        if result == A[i-1][x]:
            continue

        else:
            items.append(weight.index(weight[i-1])+ 1)
            result = result - vals[i-1]
            x = x - weight[i-1]

    return res, items

with open("shopping.txt", "r") as inFile, open("results.txt", "w") as outFile:
    tests = int(inFile.readline().strip())
    for test in range(tests):
        num_items = int(inFile.readline().strip())
        prices, weights = [], []

        for j in range(num_items):
            price, w = map(int, inFile.readline().strip().split())
            prices.append(price)
            weights.append(w)

        family = int(inFile.readline().strip())
        member_cap = [int(inFile.readline().strip()) for x in range(family)]

        total, items_chosen = 0, []
        for i in range(family):
                val, item = shoppingSpree(weights, prices, member_cap[i], num_items)
                total = total + val
                items_chosen.append(item)

        outFile.write("Test Case: %d\n" % (test + 1))
        outFile.write("Total Price: %d\n"%(total))
        outFile.write("Member Items\n")

        for y in range(0, len(items_chosen)):
            outFile.write("%d: %s"%(j + 1, " ".join(map(str, items_chosen[y]))))
            outFile.write("\n")

        outFile.write("\n")

    inFile.close()
    outFile.close()
