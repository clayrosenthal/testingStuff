from Stacks import StackArray
# Clay Rosenthal


# infix to postfix converter and postfix calculator
def infix_to_postfix(infix_expr):
	#   converts infix expression to a postfix expression
    """ Method to convert infix expressions into postix
    Infix expression should have operations and operands seperated by spaces
    postfix expression will be formatted that way"""
    expression = infix_expr.split(" ")
    # operands = StackArray(len(expression)//2)
    operands = StackArray(30)
    to_process = []
    for part in expression:
        # part = expression[i]
        if not check_num(part):
            if (part==')'):
                while (operands.peek() != '('):
                    to_process.append(str(operands.pop()))
                operands.pop()
                # print("Operand: " + part);
            else:
                while (not operandOnTop(part, operands)):
                    to_process.append(str(operands.pop()))
                operands.push(part);
                # print("Operand: " + part);
        else:
            if check_float(part):
                to_process.append(float(part))
            else:
                to_process.append(int(part))
    while (not operands.is_empty()):
        to_process.append(str(operands.pop()))
    postfix_expr = " ".join(str(thing) for thing in to_process)
    # print("Postfix Expression Ready: " + postfix_expr)
    return postfix_expr


def postfix_eval(postfix_expr):
	#   evaluates a postfix expression
    """ Evaluates a postfix expression and returns the answer """
    to_process = postfix_expr.split(" ")
    num_nums = postfix_valid(postfix_expr)
    if not num_nums:
        raise ValueError
    nums = StackArray(num_nums)
    while to_process:
        if (check_num(to_process[0])):
            nums.push(float(to_process[0]))
            del to_process[0]
            # print("Number: " + str(nums.peek()));
        else:
            # print("Operation: "+ to_process[0]);
            if to_process[0] in ["+","-","*","/","^"]:
                nums.push(do_math(nums.pop(),nums.pop(),to_process[0]))
                del to_process[0]
            else:
                del to_process[0]
            # print("Calculation complete: " + str(nums.peek()))
    return nums.pop()

def operandOnTop(operand, operands):
	#   returns true if the operand should be inserted, false if others should be popped
    """ sees if the operand being passed in should be put on the stack or have other operands pushed"""
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
	#   calculates the operation done on two operands
    """ takes in a set of numbers and the operand to compute them with"""
    if (operand=='^'):
        if num1 == 0 and num2 == 0:
            raise ValueError
        return num2**num1
    elif (operand=='*'):
        return (num2*num1)
    elif (operand=='/'):
        if num1 == 0:
            raise ValueError
        return (num2/num1)
    elif (operand=='-'):
        return num2-num1
    elif (operand=='+'):
        return num2+num1
    return num1+num2

def check_num(num):
	#  "" sees if a string is a valid number """
    """ sees if a string is a valid number """
    if num == "-":
        return False
    isNum = True
    decimal = False
    for ch in num:
        if ch not in ["0","1","2","3","4","5","6","7","8","9","-","."]:
            return False
        elif ch == ".":
            if not decimal:
                decimal = True
            else:
                return False
    return isNum

def check_float(num):
	#  "" Checks if a number is a decimal or an integer"""
    """ Checks if a number is a decimal or an integer"""
    return "." in num

def postfix_valid(postfix_expr):
	#  "" checks if a postfix expression is valid, returns None if it is false
    """ checks if a postfix expression is valid, returns None if it is false
    returns the number of numbers in the expression if it is valid"""
    to_process = postfix_expr.split(" ")
    if len(to_process) == 0:
        return None
    num_nums = 0
    num_operations = 0
    first = True
    second = False
    for token in to_process:
        if first:
            if second:
                if check_num(token):
                    first = False
                else:
                    return None
            elif check_num(token):
                second = True
            else:
                return None
        if check_num(token):
            num_nums += 1
        elif token in ["+","-","*","/","^"]:
            num_operations += 1
        else:
            continue
    if check_num(to_process[len(to_process)-1]):
        if len(to_process) == 1:
            pass
        else:
            return None
    if num_operations != (num_nums - 1):
        return None
    return num_nums