# Clay Rosenthal



# deos things the first lab required
def bin_search(target, low, high, list_val):
    # searchs binary style
    mid = ((high - low) // 2) + low
    #print("High: " + str(high) + " Low: " + str(low) + " Mid: " + str(mid))
    if (high - low) > 1:
        if target == list_val[mid]:
            return mid
        elif list_val[mid] > target:
            return bin_search(target, low, mid, list_val)
        else:
            return bin_search(target, mid, high, list_val)
    elif (high - low) == 1:
        if target == list_val[high]:
            return high
        elif target == list_val[low]:
            return low
        else:
            return None
    else:
        return None

def reverse_rec(tempstr): 
    # reverses recursively
    if len(tempstr) is 0:
        return tempstr
    if len(tempstr) is 1:
        return tempstr[0]
    else:
        return reverse_rec(tempstr[1:]) + (tempstr[0])

def max_list_iter(tlist):
    # finds the max of a list
    if len(tlist) == 0:
        raise ValueError
    maxInList = tlist[0]
    for x in tlist:
        if x > maxInList:
            maxInList = x
    return maxInList