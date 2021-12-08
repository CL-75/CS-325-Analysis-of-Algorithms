# Casey Levy
# CS 325 - HW 4 - activity.py
# Creating a program that reads input from "act.txt"

# Some code inspired by www.geeksforgeeks.org/activity-selection-problem-greedy-algo-1/

def activities(arr):
    acts = []
    for i in range(len(arr)):
        if len (acts) == 0:
            acts.append(arr[0])

        elif arr[i][2] <= acts[-1][1]:
            acts.append(arr[i])

    taken = [act[0] for act in acts]
    taken.reverse()

    return taken

def terminalOutput(case, arr):
    x = len(arr)

    print("Set %d" % (case))
    print("Number of Activities Selected = %d" % x)
    print("Activities: ", *arr)

with open("act.txt", "r") as inFile:
    acts, case = [], 1
    num_acts = inFile.readline().strip()
    while num_acts != "":
        for i in range(int(num_acts)):
            activ, set, time = map(int, inFile.readline().strip().split())
            acts.append([activ, set, time])

        acts.sort(key=lambda y: y[2], reverse = True)
        taken = activities(acts)

        terminalOutput(case, taken)
        case += 1
        acts, num_acts = [], inFile.readline().strip()


