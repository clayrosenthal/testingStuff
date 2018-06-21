# Clay Rosenthal



# testing class for queues
import unittest
import queues

class TestLab3(unittest.TestCase):

    def test_queue_array(self):
        # tests a queue implemented by an array
        queue = queues.QueueArray(5)
        self.assertEqual(queue.is_empty(), True)
        with self.assertRaises(IndexError):
            queue.dequeue()
        queue.enqueue(1)
        self.assertEqual(queue.is_empty(), False)
        queue.enqueue(2)
        queue.enqueue(3)
        self.assertEqual(queue.num_in_queue(),3)
        queue.enqueue(4)
        self.assertEqual(queue.is_full(), False)
        queue.enqueue(5)
        self.assertEqual(queue.is_full(), True)
        with self.assertRaises(IndexError):
            queue.enqueue(6)
        self.assertEqual(queue.num_in_queue(), 5)
        self.assertEqual(queue.dequeue(), 1)
        self.assertEqual(queue.dequeue(), 2)
        self.assertEqual(queue.dequeue(), 3)
        self.assertEqual(queue.dequeue(), 4)
        self.assertEqual(queue.dequeue(), 5)
        with self.assertRaises(IndexError):
            queue.dequeue()


    def test_queue_linked(self):
        # tests a queue implemented by a stack
        queue = queues.QueueLinked(5)
        self.assertEqual(queue.is_empty(), True)
        with self.assertRaises(IndexError):
            queue.dequeue()
        queue.enqueue(1)
        self.assertEqual(queue.is_empty(), False)
        queue.enqueue(2)
        queue.enqueue(3)
        self.assertEqual(queue.num_in_queue(), 3)
        queue.enqueue(4)
        self.assertEqual(queue.is_full(), False)
        queue.enqueue(5)
        self.assertEqual(queue.is_full(), True)
        with self.assertRaises(IndexError):
            queue.enqueue(6)
        self.assertEqual(queue.num_in_queue(), 5)
        self.assertEqual(queue.dequeue(), 1)
        self.assertEqual(queue.dequeue(), 2)
        self.assertEqual(queue.dequeue(), 3)
        self.assertEqual(queue.dequeue(), 4)
        self.assertEqual(queue.dequeue(), 5)
        with self.assertRaises(IndexError):
            queue.dequeue()


if __name__ == "__main__":
    unittest.main()