# Clay Rosenthal



# Test class for calulator
import unittest
import exp_eval

class TestAssign2(unittest.TestCase):

    def test_infix_to_postfix(self):
        # tests the infix to postfix converter
        self.assertEqual(exp_eval.infix_to_postfix("3 + 4 * 5"), "3 4 5 * +")
        self.assertEqual(exp_eval.infix_to_postfix("2 ^ 3 ^ 2"), "2 3 2 ^ ^")

    def test_postfix_eval(self):
        # tests the postfix calculator
        self.assertEqual(exp_eval.postfix_eval("3 4 5 * +"), 23) 
        self.assertEqual(exp_eval.postfix_eval("2 3 2 ^ ^"), 512) 

if __name__ == "__main__":
        unittest.main()
