# Clay Rosenthal
import unittest
import stacks

# test class for stacks
class TestLab2(unittest.TestCase):

    def test_stack_array(self):
        # tests stacks implemented by an array
        stack = stacks.StackArray(5)
        self.assertEqual(stack.is_empty(), True)
        with self.assertRaises(IndexError):
            stack.pop()
        with self.assertRaises(IndexError):
            stack.peek()
        stack.push(1)
        self.assertEqual(stack.is_empty(), False)
        stack.push(2)
        stack.push(3)
        self.assertEqual(stack.size(),3)
        stack.push(4)
        self.assertEqual(stack.is_full(), False)
        stack.push(5)
        self.assertEqual(stack.is_full(), True)
        with self.assertRaises(IndexError):
            stack.push(6)
        self.assertEqual(stack.size(), 5)
        self.assertEqual(stack.peek(), 5)
        self.assertEqual(stack.pop(), 5)
        self.assertEqual(stack.pop(), 4)
        self.assertEqual(stack.pop(), 3)
        self.assertEqual(stack.pop(), 2)
        self.assertEqual(stack.pop(), 1)
        with self.assertRaises(IndexError):
            stack.pop()


    def test_stack_linked(self):
        # tests stacks implemented by an linked list
        stack = stacks.StackLinked(5)
        self.assertEqual(stack.is_empty(), True)
        with self.assertRaises(IndexError):
            stack.pop()
        with self.assertRaises(IndexError):
            stack.peek()
        stack.push(1)
        self.assertEqual(stack.is_empty(), False)
        stack.push(2)
        stack.push(3)
        self.assertEqual(stack.size(), 3)
        stack.push(4)
        self.assertEqual(stack.is_full(), False)
        stack.push(5)
        self.assertEqual(stack.is_full(), True)
        with self.assertRaises(IndexError):
            stack.push(6)
        self.assertEqual(stack.size(), 5)
        self.assertEqual(stack.peek(), 5)
        self.assertEqual(stack.pop(), 5)
        self.assertEqual(stack.pop(), 4)
        self.assertEqual(stack.pop(), 3)
        self.assertEqual(stack.pop(), 2)
        self.assertEqual(stack.pop(), 1)
        with self.assertRaises(IndexError):
            stack.pop()


if __name__ == "__main__":
    unittest.main()