# Clay Rosenthal



# queue class with multiple implementations of queues
class QueueArray:
    """ Queue made with a circular array """
    def __init__(self, capacity):
        self.capacity = capacity # the maximum number of items that can be stored in queue
        self.queue_size = 0
        self.front = 0
        self.rear = 0
        self.items = [None]*self.capacity
    def is_empty(self):
        # checks if queue is empty
        return self.queue_size == 0
    def is_full(self):
        # checks if queue is full
        return self.queue_size == self.capacity
    def enqueue(self, item):
        # adds item to the back of queue
        if not self.is_full():
            self.items[self.rear] = item
            self.rear = (self.rear + 1) % self.capacity
            self.queue_size += 1
        else:
            raise IndexError
    def dequeue(self):
        # removes item from the front of queue
        if not self.is_empty():
            item = self.items[self.front]
            self.front = (self.front + 1) % self.capacity
            self.queue_size -= 1
            return item
        else:
            raise IndexError
    def num_in_queue(self):
        # returns the number of items in the queue
        return self.queue_size

class QueueLinked:
    def __init__(self, capacity):
        self.capacity = capacity # the maximum number of items that can be stored in queue
        self.queue_size = 0
        self.front = None
        self.rear = None
    def is_empty(self):
        # checks if queue is empty
        return self.queue_size == 0
    def is_full(self):
        # checks if queue is full
        return self.queue_size == self.capacity
    def enqueue(self, item):
        # adds item to the back of queue
        if not self.is_full():
            newNode = Node(data_in=item)
            if self.is_empty():
                self.front = newNode
                self.rear = newNode
                self.queue_size += 1
            else:
                self.rear.set_next(newNode)
                self.rear = newNode
                self.queue_size += 1
        else:
            raise IndexError
    def dequeue(self):
        # removes item from the front of queue
        if not self.is_empty():
            item = self.front.get_data()
            if self.queue_size == 1:
                self.front = None
                self.rear = None
                self.queue_size -= 1
            else:
                self.front = self.front.get_next()
                self.queue_size -= 1
            return item
        else:
            raise IndexError
    def queue_size(self):
        # returns the number of items in the queue
        return self.queue_size

class Node:
    """docstring for  Node"""
    def __init__(self, data_in=None, next_in=None):
        self.data = data_in
        self.next = next_in
    def set_data(self, data_in):
        # Sets the data of the node
        self.data = data_in
    def get_data(self):
        # gets the data of the ndoe
        return self.data
    def set_next(self, next_in):
        # sets the next node
        self.next = next_in
    def get_next(self):
        # gets the next node
        return self.next