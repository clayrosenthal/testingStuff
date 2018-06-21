# Clay Rosenthal
import unittest
import sep_chain_ht

# Seperate chaining hashtable tests

class TestLab8(unittest.TestCase):

    def test_seperate_chain(self):
        # tests seperate chaining
        hashtable = sep_chain_ht.MyHashTable(table_size=5)
        self.assertEqual(hashtable.size(), 0)
        hashtable.insert(5, "five")
        hashtable.insert(4, "four")
        hashtable.insert(3, "three")
        hashtable.insert(54, "fifty four")
        hashtable.insert(25, "twenty five")
        hashtable.insert(5, "five part two")
        self.assertEqual(hashtable.size(), 5)
        self.assertEqual(hashtable.collisions(), 2)
        self.assertEqual(hashtable.get(5), (5, "five part two"))
        self.assertEqual(hashtable.load_factor(), 1)
        hashtable.insert(6, "six")
        hashtable.insert(1, "one")
        self.assertEqual(hashtable.load_factor(), 1.4)
        hashtable.insert(2, "two")
        hashtable.insert(9, "nine")
        hashtable.insert(17, "tenty seven")
        hashtable.insert(33, "thirty three")
        self.assertEqual(hashtable.load_factor(), 1)
        self.assertEqual(hashtable.size(), 11)
        self.assertEqual(hashtable.remove(4), (4, "four"))
        with self.assertRaises(LookupError):
            hashtable.remove(77)
        with self.assertRaises(LookupError):
            hashtable.get(77)




if __name__ == "__main__":
        unittest.main()