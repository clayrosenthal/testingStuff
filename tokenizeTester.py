from tokenize import tokenize, COMMENT, generate_tokens, STRING

tokenFile = open("heap_lab.py", "rb").next

# print(tokenFile)


tokenStuff = generate_tokens(tokenFile)

# for token in tokenStuff:
#     print token

for toknum, tokval, strt, end, line in tokenStuff:
    if toknum == COMMENT:
        print tokval
    else if toknum == STRING:
        print tokval

#while tokenLine is not None:
    #token = tokenize(tokenLine)
    #print(tokenLine)
    #tokenLine = tokenFile.readline()
    # token = tokenize.tokenize(tokenLine)
    # if token is tokenize.COMMENT:
    #     print(token)
