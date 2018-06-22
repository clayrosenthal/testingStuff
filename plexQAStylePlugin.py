import astroid
import tokenize
 
from pylint.interfaces import IAstroidChecker
from pylint.checkers import BaseChecker
 
 
class checksForHeader(BaseChecker):
    """checker to check if a file has a header"""
    __implements__ = IAstroidChecker
 
    name = 'header-missing-checker'
 
    HEADER_WARNING = 'header-incorrect'
    
    # here we define our messages
    msgs = {
        'W0420': ('Standard header is missing %s',
                  HEADER_WARNING,
                  'Refer to project rules on wiki'),
    }
    options = ()
 
    priority = -1
 
    def visit_module(self, node):
        """Defines what pylint should look for in the header"""
        headerStartDefault = "#==============================================================================="
        tokenFile = open(str(node.file), "rb").next
        tokenStuff = tokenize.generate_tokens(tokenFile)

        barsCheck = False
        createCheck = False
        authorCheck = False
        descCheck = False

        for toknum, tokval, strt, end, line in tokenStuff:
            if ((strt[0] == 1 or strt[0] == 6) and 
                    (toknum != tokenize.COMMENT and toknum != tokenize.NL)
                    and headerStartDefault not in line and not barsCheck):

                # print "bars:", toknum, tokenize.COMMENT
                barsCheck = True
                args = "bars on line " + str(strt[0])
                self.add_message(
                    self.HEADER_WARNING, node=node, args=args
                )
            elif (strt[0] == 2 and 
                    (toknum != tokenize.COMMENT and toknum != tokenize.NL)
                    and "Created on:" not in line and not createCheck):

                # print "create:", toknum, tokenize.COMMENT
                createCheck = True
                args = "creation date on line " + str(strt[0])
                self.add_message(
                    self.HEADER_WARNING, node=node, args=args
                )
            elif (strt[0] == 3 and 
                    (toknum != tokenize.COMMENT and toknum != tokenize.NL)
                    and "Author:" not in line and not authorCheck):

                # print "author:", toknum, tokenize.COMMENT
                authorCheck = True
                args = "author on line " + str(strt[0])
                self.add_message(
                    self.HEADER_WARNING, node=node, args=args
                )
            elif (strt[0] == 5 and 
                    (toknum != tokenize.COMMENT and toknum != tokenize.NL)
                    and not descCheck):

                descCheck = True
                # print "description:", toknum, tokenize.COMMENT
                args = "description on line " + str(strt[0])
                self.add_message(
                    self.HEADER_WARNING, node=node, args=args
                )
 
def register(linter):
    """required method to auto register this checker"""
    linter.register_checker(checksForHeader(linter))