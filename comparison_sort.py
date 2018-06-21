# Clay Rosenthal



# comparing sorting algorythyms

def insertion_sort(alist):
    # insertion sort method
    compCount = 0
    for index in range(1,len(alist)):

        currentvalue = alist[index]
        position = index
        compCount += 1
        while position>0 and alist[position-1]>currentvalue:
            compCount += 1
            alist[position] = alist[position-1]
            position = position-1

        alist[position]=currentvalue

    return compCount

def selection_sort(alist):
    # sorts via selction sort
    compCount = 0
    for fillslot in range(len(alist)-1,0,-1):
        positionOfMax=0
        for location in range(1,fillslot+1):
            compCount += 1
            if alist[location]>alist[positionOfMax]:
                positionOfMax = location

        temp = alist[fillslot]
        alist[fillslot] = alist[positionOfMax]
        alist[positionOfMax] = temp

    return compCount

def merge_sort(alist):
    # sorts a list with merge sort
    if len(alist) == 1:
        return 0
    else:
        compCount = 0
        blist = list(alist[0:len(alist)//2])
        clist = list(alist[len(alist)//2:])
        compCount += merge_sort(blist)
        compCount += merge_sort(clist)

        return compCount + merge(alist, blist, clist)


def merge(alist, blist, clist):
    # merges two lists into one
	#   merges two lists into one
    i, j, k = 0, 0, 0
    compCount = 0
    while j < len(blist) and k < len(clist):
        if blist[j] <= clist[k]:
            alist[i] = blist[j]
            j += 1
        else:
            alist[i] = clist[k]
            k += 1
        compCount += 1
        i += 1
    while j < len(blist):
        alist[i] = blist[j]
        i, j = i+1, j+1
    while j < len(blist):
        alist[i] = blist[j]
        i, j = i+1, j+1
    return compCount



sets = {"test_1" : [7, 6, 14, 20, 13, 19, 16, 2, 10, 5, 8, 18, 12, 15, 4, 17, 9, 3, 0, 11],
        "test_2" : [1, 13, 20, 18, 15, 2, 7, 9, 11, 8, 19, 16, 4, 17, 10, 5, 14, 3, 0, 6], 
        "test_3" : [2, 3, 14, 0, 17, 16, 8, 13, 4, 1, 11, 9, 19, 5, 6, 18, 7, 12, 20, 15],
        "test_4" : [15, 2, 8, 4, 3, 0, 7, 19, 12, 17, 6, 13, 1, 14, 18, 20, 9, 5, 16, 11],
        "test_5" : [12, 17, 6, 20, 13, 14, 18, 4, 16, 1, 9, 7, 8, 15, 10, 3, 5, 11, 2, 0],
        "test_6" : [2, 15, 1, 5, 0, 7, 17, 3, 4, 18, 12, 10, 11, 20, 19, 13, 9, 16, 8, 14], 
        "test_7" : [17, 13, 20, 5, 3, 2, 15, 1, 18, 6, 19, 11, 10, 9, 8, 16, 12, 7, 4, 14],
        "test_8" : [11, 13, 18, 4, 2, 10, 16, 1, 0, 6, 3, 5, 7, 12, 8, 15, 9, 20, 19, 17],
        "test_9" : [16, 7, 10, 8, 13, 2, 1, 0, 19, 14, 15, 9, 18, 4, 5, 17, 20, 6, 11, 12],
        "test_10" : [11, 2, 3, 14, 19, 9, 6, 5, 10, 15, 12, 18, 0, 20, 13, 8, 7, 4, 16, 17],
        "test_11" : [7, 20, 2, 1, 10, 9, 12, 8, 0, 4, 16, 18, 13, 3, 5, 17, 11, 6, 15, 14],
        "test_12" : [1, 15, 8, 9, 16, 18, 17, 11, 5, 3, 6, 19, 4, 12, 14, 2, 13, 0, 7, 20],
        "test_13" : [11, 2, 5, 3, 18, 14, 0, 10, 6, 1, 15, 13, 17, 19, 7, 16, 12, 4, 9, 20],
        "test_14" : [0, 19, 6, 15, 17, 13, 11, 5, 1, 4, 20, 16, 2, 7, 8, 14, 9, 18, 3, 12],
        "test_15" : [4, 1, 5, 16, 12, 7, 20, 13, 15, 3, 9, 2, 0, 14, 11, 18, 19, 17, 10, 6],
        "test_16" : [6, 9, 10, 15, 8, 11, 7, 12, 3, 19, 17, 0, 1, 5, 2, 14, 16, 13, 18, 20],
        "test_17" : [0, 2, 6, 13, 9, 11, 7, 1, 15, 3, 5, 19, 17, 18, 12, 8, 14, 4, 16, 10],
        "test_18" : [17, 19, 13, 7, 20, 15, 3, 14, 16, 10, 2, 4, 1, 6, 12, 9, 5, 11, 0, 8],
        "test_19" : [4, 1, 11, 14, 12, 3, 9, 10, 13, 6, 17, 5, 8, 19, 16, 15, 0, 18, 20, 2],
        "test_20" : [15, 5, 9, 4, 2, 11, 17, 10, 8, 12, 3, 20, 6, 16, 0, 18, 7, 13, 19, 14],
        "test_insertion_worst_20" : list(range(20,0,-1)),
        "test_selection_worst_20" : list(range(0,20,1)),
        "test_insertion_worst_40" : list(range(40,0,-1)),
        "test_selection_worst_40" : list(range(0,40,1)),
        "test_insertion_worst_60" : list(range(60,0,-1)),
        "test_selection_worst_60" : list(range(0,60,1)),
        "test_insertion_worst_80" : list(range(80,0,-1)),
        "test_selection_worst_80" : list(range(0,80,1)),
        "test_insertion_worst_100" : list(range(100,0,-1)),
        "test_selection_worst_100" : list(range(0,100,1))}
fileToOpen = open("compareTests.txt", "w")
for name, test in sets.items():
    print(name)
    fileToOpen.writelines("\n"+name)
    unsorted = test[:]
    print("Unsorted: " + str(unsorted))
    fileToOpen.writelines("\nUnsorted: " + str(unsorted))
    print("Insertion Comparisons: " + str(insertion_sort(test)))
    test = unsorted[:]
    fileToOpen.writelines("\nInsertion Comparisons: " + str(insertion_sort(test)))
    test = unsorted[:]
    print("Selection Comparisons: " + str(selection_sort(test)))
    test = unsorted[:]
    fileToOpen.writelines("\nSelection Comparisons: " + str(selection_sort(test)))
    test = unsorted[:]
    print("Merge Comparisons: " + str(merge_sort(test)))
    test = unsorted[:]
    fileToOpen.writelines("\nMerge Comparisons: " + str(merge_sort(test)))
    test = unsorted[:]

fileToOpen.close()

"""
The tests are worst case for insertion when they are the reverse of the order you want,
as they will have to compare against every prior value in the list every time.
Selection sort has a constant worse case as selection has to always look through all the items
Merge sorts have a much more consistent case by case number of comparisons
"""