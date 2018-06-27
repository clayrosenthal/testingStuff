from hash_lin_table import *
from hash_quad_table import *
import filecmp


def filecompare(file1, file2):
    f1 = open(file1, "r")
    f2 = open(file2, "r")
    for l1 in f1.readlines():
        if l1 != f2.readline():
            return False
    return True

# Create stop words hash table
stop_words = HashTableQuadPr(251)            # start with table size of 251, grow as needed
stop_words.read_stop('stop_words.txt')      # read in stop words, load hash table

# Create concordance hash table
concord1 = HashTableQuadPr(251)               # start with table size of 251, grow as needed
concord1.read_file('input1.txt',stop_words)  # read from file, process as required, load hash table
concord1.save_concordance('test1.txt')       # save (write) concordance to file

# print(stop_words.get_table())
# print(concord.get_table())

# Compare test1.txt file to known good concord1.txt file
print("File compare 1:", filecmp.cmp('test1.txt','concord1.txt')) # will be True if files match
print("File line by line compare 1:", filecompare('test1.txt','concord1.txt'))
# Create concordance hash table
concord2 = HashTableLinPr(251)               # start with table size of 251, grow as needed
concord2.read_file('input2.txt',stop_words)  # read from file, process as required, load hash table
concord2.save_concordance('test2.txt')       # save (write) concordance to file

# print(stop_words.get_table())
# print(concord.get_table())

# Compare test1.txt file to known good concord1.txt file
print("File compare 2:", filecmp.cmp('test2.txt','concord2.txt')) # will be True if files match
print("File line by line compare 2:", filecompare('test2.txt','concord2.txt'))


concord3 = HashTableLinPr(251)               # start with table size of 251, grow as needed
concord3.read_file('input3.txt',stop_words)  # read from file, process as required, load hash table
concord3.save_concordance('test3.txt')

# print(concord3.get_table())