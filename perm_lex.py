# Clay Rosenthal
def perm_gen_lex(a): 
    """ Returns all possible permutations of a string of distinct alphabetic characters """
   
    # case for a string that is a single character
    if len(a) == 1:
        return [a]
    else:
        # create an array to hold all permutations in the future
        perms = []
        # iterate through every character in input string
        for ch in a:
            # remove character from input string
            new_str = a.replace(ch,"")
            # recursively iterate over new string that doesnt have current character
            new_perms = perm_gen_lex(new_str)
            # add character to front of new permutations
            # add new permutations to existing permutations
            for perm in new_perms:
                perms.append(ch+perm)
        # returns the complete set of permutations
        return perms