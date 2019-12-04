# Clay Rosenthal



# infix to postfix converter and postfix calculator
def infix_to_postfix(expressionRaw):
    # converts infix expression to a postfix expression
    expression = expressionRaw.split(" ")
    operands = StackLinked(len(expression)//2)
    numsCounter = 0
    to_process = []
    for part in expression:
        # part = expression[i]
        if not part.isdigit():
            if (part==')'):
                while (operands.peek() != '('):
                    to_process.append(str(operands.pop()))
                operands.pop()
                print(("Operand: " + part));
            else:
                while (not operandOnTop(part, operands)):
                    to_process.append(str(operands.pop()))
                operands.push(part);
                print(("Operand: " + part));
        else:
            numsCounter += 1
            to_process.append(int(part))
    while (not operands.is_empty()):
        to_process.append(str(operands.pop()))
    postfix_expression = " ".join(str(thing) for thing in to_process)
    print(("Postfix Expression Ready: " + postfix_expression))
    return postfix_expression


def postfix_eval(expression):
    # evaluates a postfix expression
    to_process = expression.split(" ")
    nums = StackLinked(len(expression)//2)
    while to_process:
        if (to_process[0].isdigit()):
            nums.push(int(to_process[0]))
            del to_process[0]
            print(("Number: " + str(nums.peek())));
        else:
            print(("Operation: "+ to_process[0]));
            nums.push(do_math(nums.pop(),nums.pop(),to_process[0]))
            del to_process[0]
            print(("Calculation complete: " + str(nums.peek())))
    return nums.pop()


def operandOnTop(operand, operands):
    # returns true if the operand should be inserted, false if others should be popped
    if (operands.is_empty()):
        return True
    top = operands.peek()
    if (operand=='('):
        return True
    elif (operand=='^' and top =='^'):
        return True
    elif ((operand=='*'or operand=='/') and not (top=='^'or top=='*'or top=='/')):
        return True
    elif ((operand=='-' or operand=='+') and not(top=='^' or top=='*' or top=='/' or top=='-' or top=='+')):
        return True
    else:
        return False

def do_math(num1, num2, operand):
    # calculates the operation done on two operands
    if (operand=='^'):
        return num2**num1
    elif (operand=='*'):
        return (num2*num1)
    elif (operand=='/'):
        return (num2/num1)
    elif (operand=='-'):
        return num2-num1
    elif (operand=='+'):
        return num2+num1
    return num1+num2



class StackLinked:
    """Implements an efficient last-in first-out Abstract Data Type using a Python List"""

    def __init__(self, capacity):
        """Creates and empty stack with a capacity"""
        self.capacity = capacity
        self.top = None
        self.num_items = 0

    def is_empty(self):
	#   returns true if list is empty
        """Returns true if the stack self is empty and false otherwise"""
        return (self.num_items == 0)
 
    def is_full(self):
	#  ""Returns true if the stack self is full and false otherwise"""
        """Returns true if the stack self is full and false otherwise"""
        return (self.num_items == self.capacity)
 
    def push(self, item):
	#  "" Pushes an item onto the top of the stack """
        """ Pushes an item onto the top of the stack """
        if not self.is_full():
            temp = Node(data_in=item, next_in=self.top)
            self.top = temp
            self.num_items += 1
        else:
            raise IndexError
 
    def pop(self):
	#   removes an item from either the end of an index and returns the item
        """Returns item on the top of the stack and removes it"""
        if not self.is_empty():
            temp = self.top.get_data()
            self.top = self.top.get_next()
            self.num_items -= 1
            return temp
        else:
            raise IndexError
 
    def peek(self):
	#  ""Returns item on the top of the stack but does not remove it"""
        """Returns item on the top of the stack but does not remove it"""
        if not self.is_empty():
            return self.top.get_data()
        else:
            raise IndexError

    def size(self):
	#  returns number of items in table
       """Returns the number of items in the stack"""
       return self.num_items

class Node:

    def __init__(self, data_in=None, next_in=None):
        self.data = data_in
        self.next = next_in
    def set_data(self, data_in):
        # sets the data in a node
        self.data = data_in
    def get_data(self):
        # gets the data in a node
        return self.data
    def set_next(self, next_in):
        # sets the next node
        self.next = next_in
    def get_next(self):
        # gets the next node
        return self.__next__