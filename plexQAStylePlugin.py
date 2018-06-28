from pylint.interfaces import IRawChecker
from pylint.checkers import BaseChecker


class checksForHeader(BaseChecker):
    """checker to check if a file has a header"""
    __implements__ = IRawChecker

    name = 'header-missing-checker'

    HEADER_WARNING = 'header-incorrect'

    # here we define our messages
    msgs = {
        'C0411': ('Standard header is missing %s',
                  HEADER_WARNING,
                  'Refer to project rules on wiki'),
    }
    options = ()

    priority = -10


    def process_module(self, node):
        """defining what to look for in the header of the file"""
        headerStartDefault = (
        "#===============================================================================")
        with node.stream() as stream:
            for (linenum, line) in enumerate(stream):
                if (linenum == 0 or linenum == 5) and headerStartDefault not in line:
                    args = "bars on line " + str(linenum+1)
                    self.add_message(
                        self.HEADER_WARNING, args=args, line=linenum
                    )
                elif linenum == 1 and "Created on:" not in line:
                    args = "creation date on line " + str(linenum+1)
                    self.add_message(
                        self.HEADER_WARNING, args=args, line=linenum
                    )
                elif linenum == 2 and "Author:"  not in line:
                    args = "author on line " + str(linenum+1)
                    self.add_message(
                        self.HEADER_WARNING, args=args, line=linenum
                    )
                elif linenum == 4 and "# " not in line:
                    args = "description on line " + str(linenum+1)
                    self.add_message(
                        self.HEADER_WARNING, args=args, line=linenum
                    )


def register(linter):
    """required method to auto register this checker"""
    linter.register_checker(checksForHeader(linter))