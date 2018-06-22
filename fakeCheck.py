import astroid
 
from pylint.interfaces import IAstroidChecker
from pylint.checkers import BaseChecker
 
 
class fakeCheck(BaseChecker):
    """checker to check if a file has a header"""
    __implements__ = IAstroidChecker
 
    name = 'fake-checker'
 
    FAKE_WARNING = 'fake-warning'
 
    # here we define our messages
    msgs = {
        'C1234': ('Fake plugin',
                  FAKE_WARNING,
                  'Hopefully we can find this'),
    }
    options = ()
 
    priority = -1
 
    def visit_module(self, node):
        """Just trying stuff"""
        print "Found me!"
 
def register(linter):
    """required method to auto register this checker"""
    linter.register_checker(fakeCheck(linter))