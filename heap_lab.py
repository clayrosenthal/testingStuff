#================
# sample header
#================
"""docstring is here"""
# Clay Rosenthal

import os


# heap and heapsort class

class MaxHeap():
    def __init__(self, capacity=50):
        self.heap = [None]*(capacity+1)
        self.capacity = capacity
        self.heap[0] = 0

    def insert(self, item):
        # inserts item into heap returns true if successful, false if no room
	#  ""  Insert new node with key, assumes data not present """
        if self.heap[0] + 1 > self.capacity:
            return False
        self.heap[0] += 1
        self.heap[self.heap[0]] = item
        self.perc_up(self.heap[0])
        return True


    def find_max(self): 
        # returns max without changing the heap
        return self.heap[1]

    def del_max(self): 
        # returns max and removes it from the heap and restores the heap property
        if self.is_empty():
            raise ValueError
        rtn = self.heap[1]
        self.heap[0] -= 1
        self.heap[1] = self.heap[self.heap[0]+1]
        if self.heap[0] > 0:
            self.perc_down(1)
        return rtn

    def heap_contents(self): 
        # returns a list of contents of the heap in the order it is stored internal to the heap. (This may be useful for in testing your implementation.)
        return self.heap[1:self.heap[0]+1]

    def build_heap(self, alist):
        """ Method build_heap that has a single explicit argument “list of int” and builds a heap using the bottom up method discussed in class. It should return True if the build was successful and False if the capacity of the MaxHeap object is not large enough to hold the “array of int” argument.
        """
        if len(alist) > self.capacity:
            return False
        i = len(alist) // 2
        self.heap = [len(alist)] + alist[:]
        while i > 0:
            self.perc_down(i)
            i -= 1
        return True

    def is_empty(self):
        # returns True if the heap is empty, false otherwise
        return self.heap[0] is 0

    def is_full(self): 
        # returns True if the heap is full, false otherwise
        return self.heap[0] is self.capacity

    def get_heap_cap(self):
        # this is the maximum number of a entries the heap can hold - 1 less than the number of entries that the array allocated to hold the heap can hold.
        return self.capacity

    def get_heap_size(self):
        # the actual number of elements in the heap, not the capacity
        return self.heap[0]

    def perc_down(self, i):
        """ where the parameter i is an index in the heap and perc_down moves the
        element stored at that location to its proper place in the heap rearranging elements as it goes.
        Since this is an internal method we will assume that the element is either in the correct position
        or the correct position is below the current position. 
        """
        left, right, maxIndex = i * 2, i * 2 + 1, 0
        if right > self.heap[0]:
            if left > self.heap[0]:
                return False
            else:
                maxIndex = left
        else:
            if self.heap[left] >= self.heap[right]:
                maxIndex = left
            else:
                maxIndex = right
        if self.heap[i] < self.heap[maxIndex]:
            temp = self.heap[maxIndex]
            self.heap[maxIndex] = self.heap[i]
            self.heap[i] = temp
        self.perc_down(maxIndex)
        return True

    
    def perc_up(self, i):
        """similar specification as perc_down, see class notes
Normally these would be private but make them public for testing purposes"""
        if i != 1:
            parent = i // 2
            if self.heap[parent] < self.heap[i]:
                temp = self.heap[parent]
                self.heap[parent] = self.heap[i]
                self.heap[i] = temp
                self.perc_up(parent)


    def heap_sort_increase(self, alist):
        # takes a list of integers and returns a list containing the integers in nondecreasing order using the Heap Sort algorithm
        self.build_heap(alist)
        while self.heap[0] > 0:
            temp = self.del_max()
            self.heap[self.heap[0]+1] = temp
        return self.heap[1:len(alist)+1]