import astroid
import tokenize
 
from pylint.interfaces import IAstroidChecker
from pylint.checkers import BaseChecker
 
 
class checksForHeader(BaseChecker):
    """checker to check if a file has a header"""
    __implements__ = IAstroidChecker
 
    name = 'header-missing-checker'
 
    HEADER_WARNING = 'header-missing'
 
    DIR_HIGHER = 'higher'
    DIR_LOWER = 'lower'
    # here we define our messages
    msgs = {
        'C5123': ('Standard header is missing',
                  HEADER_WARNING,
                  'Refer to project rules on wiki'),
    }
    options = ()
 
    priority = -1
 
    def visit_module(self, node):
        headerStartDefault = "#==============================================================================="
        tokenFile = open(str(node.file), "rb").next
        tokenStuff = tokenize.generate_tokens(tokenFile)

        for toknum, tokval, strt, end, line in tokenStuff:
            if toknum == tokenize.COMMENT:
                if strt[0] == 1 and tokval != headerStartDefault:
                    args = node.as_string(), tokval
                    self.add_message(
                        self.HEADER_WARNING, node=node
                    )
 
def register(linter):
    """required method to auto register this checker"""
    linter.register_checker(checksForHeader(linter))