# ===============================================================================
# Created on: October 16, 2017
# Author: Clay Rosenthal
#
# This script was created to generate proper comments for the readmegen into existing files
# ===============================================================================

from os import listdir, getcwd, remove, walk
from os.path import isfile, join, dirname, realpath

class REVERSEREADME():
    """Reinserts descriptions from readme files"""
    def scanForMethods(self,fileName ,methods):
        """scans a given file for methods and adds descriptions as necessary"""
        num_lines = sum( 1 for line in open(fileName))
        fileToRead = open(fileName, "r")
        fileToWrite = open(fileName.replace(".py","readMed.py"), "w")
        methodName = ""
        wasMethod = False
        for x in range(num_lines):
            line = fileToRead.readline()
            if "def" in line and "# ignore" not in line: # ignore
                methodName = ""
                usefulInfo = False
                notInit = True
                defStart = 0 # ignore
                for i in range(len(line)):
                    ch = line[i]
                    if usefulInfo:
                        if ch == "_" and line[i:i+6] == "__init":
                            notInit = False
                        if ch is not "(" and i > (defStart+3): # ignore
                            methodName = methodName + ch
                        elif ch is "(":
                            usefulInfo = False
                    else:
                        if ch == "d" and line[i:i+3] == "def": # ignore
                            defStart = i # ignore
                            usefulInfo = True
                        if ch is ":":
                            wasMethod = True
            if methodName in methods and wasMethod and (methodName+"(self") not in line:
                if "\"\"\"" not in line: # or '"""' not in line:
                    fileToWrite.write("        \"\"\"%s\"\"\"\n" % methods[methodName])
                methodName = ""
                wasMethod = False
            elif methodName not in methods and wasMethod:
                methodName = ""
                wasMethod = False
            fileToWrite.write(line)
                
        fileToRead.close()
        fileToWrite.close()
        
        fileToWrite = open(fileName, "w")
        fileToRead = open(fileName.replace(".py","readMed.py"), "r")
        for line in fileToRead.readlines():
            fileToWrite.write(line)

        fileToRead.close()
        fileToWrite.close()
        remove(fileName.replace(".py","readMed.py"))


    def getReadMeInfo(self,fileName):
        """gets the readMe methods and descriptions"""
        fileToOpen = open(fileName, "r")
        isFunctionSet = False
        methods = {}
        for line in fileToOpen.readlines():


            if isFunctionSet:
                if "|" not in line:
                    isFunctionSet = False
                elif "-|-" in line:
                    pass
                else:
                    methodName = ""
                    description = ""
                    isMethod = True
                    for ch in line:
                        if ch is "|":
                            isMethod = False
                        elif ch is not " ":
                            if isMethod:
                                methodName += ch
                            else:
                                description += ch
                        else:
                            if not isMethod:
                                description += ch
                    methods.update({ methodName : description.strip('\n').lstrip().replace('"', '\'') })

            if ("function" in line.lower() or "test case" in line.lower()) and "description" in line.lower():
                isFunctionSet = True

        fileToOpen.close()




        return methods






    def __correctFiles( self ):
        """corrects files in a given path to be ready for readme generation"""
        for path, subdirs, files in walk(getcwd()):
            try:
                


                methods = self.getReadMeInfo(join(path, "README.md"))
            except IOError:
                continue
            for name in files:
                file = join(path, name)
                if (".py" in file and ".pyc" not in file  and "readMed.py" not in file):
                    self.scanForMethods(file, methods)
                else:
                    pass


    def USELESSTRASH(        self        ): 

        try:
            print "dumb stuff"
        except:
            print "oh well"
