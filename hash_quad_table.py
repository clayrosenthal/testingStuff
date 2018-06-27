# Clay Rosenthal

import string

# gets a list of words and their line numbers

class HashTableQuadPr:

    def __init__ (self, size=251): # creates and initializes the hash table size to size
        self.filled = 0
        self.table = [None]*size


    def get_tablesize(self): # returns the size of the hash table
        return len(self.table)
    

    def get_load_fact(self): # returns the load factor of the table
        return self.filled / len(self.table)


    def my_hash(key, table_size):
        # computes a hash
        hash_val = 0
        length = len(key)-1 if len(key)-1 < 8 else 8
        for i in range(length, 0, -1):
            hash_val = hash_val*31 + ord(key[i])
        return hash_val % table_size


    def insert(self, key, item):
	#  ""  Insert new node with key, assumes data not present """
        hash_val = self.myhash(key, len(self.table))
        self.filled += 1
        if self.get_load_fact() > .5:
            self.rehash()
        odd = 1
        while self.table[hash_val] is not None and key != self.table[hash_val][0]:
            hash_val = (hash_val + odd) % self.get_tablesize()
            odd = odd + 2
        if self.table[hash_val] is None:
            self.table[hash_val] = [key, [item]]
        else:
            self.table[hash_val][1].append(item)


    def rehash(self): # rearrange elements
	#  doubles the table size and reassigns the keys
        new_table = HashTableQuadPr(size=len(self.table)*2+1)
        for element in self.table:
            if element is not None:
                for item in element[1]:
                    new_table.insert(element[0], item)
        self.table = new_table.get_table()[:]


    def get_table(self):
        return self.table


    def read_stop (self, filename): # read words from a stop words file and insert them into hash table
        fileToOpen = open(filename, "r")
        for line in fileToOpen.readlines():
            line = find_words(line)[0]
            self.insert(line, line)
        fileToOpen.close()

    def find(self, key):
        # returns True if key is in table
        for element in self.table:
            if element is not None and element[0] == key:
                return True
        return False

    def get(self, key):
        # returns key item pair or raise LookupError
        for element in self.table:
            if element is not None and element[0] == key:
                return element
        raise LookupError

    def read_file (self, filename, stop_table): # read words from input file and insert them into hash table,
        # after processing for punctuation, numbers and filtering out stop words in the stop_table
        fileToOpen = open(filename, "r")
        lineNum = 1
        for line in fileToOpen.readlines():
            words = find_words(line)
            for word in words:
                if not stop_table.find(word):
                    self.insert(word, lineNum)
            lineNum += 1
        fileToOpen.close()

    def find_words(line):
        word = ""
        words = []
        for ch in line:
            if ch in string.ascii_letters:
                word += ch.lower()
            else:
                if ch in [" ", "-", "."] and word is not "":
                    if word not in words:
                        words.append(word)
                    word = ""
                else:
                    pass
        if word is not "" and word not in words:
            words.append(word)
        return words

    def save_concordance(self, outputfilename):  # see sample output files for format
        fileToOpen = open(outputfilename, "w")
        words = []
        for element in self.table:
            if element is not None:
                words.append(pair_to_string(element[0], element[1]))
        words.sort()
        lines = []
        for word in words:
            lines.append(word)
        fileToOpen.write("\n".join(lines))
        fileToOpen.close()


    def pair_to_string(key, items):
        return key + ":\t" + " ".join(str(item) for item in items)