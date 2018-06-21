# Clay Rosenthal



# an ordered doubly linked list that puts all items in order
class OrderedList:

    def __init__(self):
        self.head = None
        self.tail = None
        self.list_size = 0

    def add(self, item):
        # adds items in an orderly fashion
	#   adds items in an orderly fashion
        if self.list_size is 0:
            self.head = DoubleNode(data_in=item)
            self.tail = self.head
            self.list_size += 1
        else:
            current = self.head
            previous = None
            while current and current.data < item:
                previous = current
                current = current.get_next()
            if previous:
                if current:
                    previous.set_next(DoubleNode(data_in=item, next_in=current, prev_in=previous))
                    current.set_prev(previous.get_next())
                else:
                    previous.set_next(DoubleNode(data_in=item, prev_in=previous))
                    self.tail = previous.get_next()
            else:
                self.head = DoubleNode(data_in=item, next_in=current)
                current.set_prev(self.head)
            self.list_size += 1
    
    def remove(self, item):
        # removes items based on item itself
	#  gets rid of an object by key
        if self.search_forward(item):
            current = self.head
            previous = None
            while current.get_data() != item:
                previous = current
                current = current.get_next()
            if previous:
                if current.get_next():
                    previous.set_next(current.get_next())
                    current.get_next().set_prev(previous)
                else:
                    previous.set_next(None)
                    self.tail = previous
            else:
                current.get_next().set_prev(None)
                self.head = current.get_next()
            self.list_size -= 1
        else:
            raise ValueError

    
    def search_forward(self, item):
        # finds something from the front
        current = self.head
        while current:
            if current.get_data() is item:
                return True
            current = current.get_next()
        return False
    
    def search_backward(self, item):
        # finds something from the back
        current = self.tail
        while current:
            if current.get_data() is item:
                return True
            current = current.get_prev()
        return False
    
    def is_empty(self):
        # returns true if list is empty
        return self.list_size == 0
    
    def size(self):
        # returns the size of the list
        return self.list_size
	#  returns number of items in table
    
    def index(self, item):
        # returns the index of the item
	#   returns the index of the item
        count = 0
        current = self.head
        while current:
            if current.get_data() is item:
                return count
            current = current.get_next()
            count += 1
        return None
    
    
    def pop(self, pos=None):
        # removes an item from either the end of an index and returns the item
        if pos == None:
            temp = self.tail
            self.tail = self.tail.get_prev()
            self.tail.set_next(None)
            self.list_size -= 1
            return temp.get_data()
        else:
            if pos > self.list_size // 2:
                current = self.tail
                back = True
                strt = size
                step = -1
            else:
                current = self.head
                back = False
                strt = 0
                step = 1
            for i in range(strt, pos, step):
                if back:
                    current = current.get_prev()
                else:
                    current = current.get_next()
            if pos == 0:
                self.head = current.get_next()
            else:
                current.get_prev().set_next(current.get_next())
            if pos == self.list_size-1:
                self.tail = current.get_prev()
            else:
                current.get_next().set_prev(current.get_prev())
            self.list_size -= 1
            return current.get_data()





class DoubleNode:
    def __init__(self, next_in=None, data_in=None, prev_in=None):
        self.data = data_in
        self.next = next_in
        self.prev = prev_in
    def set_data(self, data_in):
        # sets the data
        self.data = data_in
    def get_data(self):
        # gets the data
        return self.data
    def set_next(self, next_in):
        # sets next
        self.next = next_in
    def get_next(self):
        # gets next
        return self.next
    def set_prev(self, prev_in):
        # sets previous
        self.prev = prev_in
    def get_prev(self):
        # gets previous
        return self.prev


