# Clay Rosenthal



# creates a hasttable by seperate chaining

class MyHashTable:

    def __init__(self, table_size=11):
        # self.table = [[] for i in range(table_size)]
        self.table = [None] * table_size
        self.filled = 0
        self.col = 0

    def insert(self, key, item):
	#  ""  Insert new node with key, assumes data not present """

        hash_value = self.hash(key)
        if self.table[hash_value] is None:
            self.table[hash_value] = Node(key_in=key, item_in=item)
            self.filled += 1
        else:
            temp = self.table[hash_value]
            while temp.next is not None:
                if temp.key is key:
                    temp.item = item
                    break
                temp = temp.next
            if temp.next is None:
                temp.next = Node(key_in=key, item_in=item)
                self.filled += 1
                self.col += 1
        
        if self.load_factor() > 1.5:
             self.rehash()


    def get(self, key):
        hash_value = self.hash(key)
        rtn = self.table[hash_value]
        while rtn is not None and rtn.key != key:
            rtn = rtn.next
        if rtn is None:
            raise LookupError
        return rtn.key, rtn.item


    def remove(self, key):
	#  gets rid of an object by key
        hash_value = self.hash(key)
        prev = None
        rtn = self.table[hash_value]
        while rtn is not None and rtn.key != key:
            prev = rtn
            rtn = rtn.next
        if rtn is None:
            raise LookupError
        if prev is not None:
            prev.next = rtn.next
        else:
            self.table[hash_value] = rtn.next
        return rtn.key, rtn.item


    def size(self):
	#  returns number of items in table
        return self.filled


    def load_factor(self):
	#  returns number of items in table divided by size
        return self.filled / len(self.table)


    def collisions(self):
	#  returns number of collisions in the table
        return self.col


    def hash(self, key):
	#  takes a key and returns a hash value
        return key % len(self.table)


    def rehash(self):
	#  doubles the table size and reassigns the keys
        new_table = MyHashTable(table_size=(len(self.table) * 2 + 1))
        for i in range(len(self.table)):
            while self.table[i] is not None:
                to_insert = self.remove(self.table[i].key)
                new_table.insert(to_insert[0], to_insert[1])
        self.col += new_table.collisions()
        self.table = new_table.ret_table()

            
    def ret_table(self):
	#  returns the table
        return self.table


class Node:

    def __init__(self, key_in=None, item_in=None, next_in=None):
        self.key = key_in
        self.item = item_in
        self.next = next_in
