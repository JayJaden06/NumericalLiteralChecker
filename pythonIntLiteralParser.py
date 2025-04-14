""" python numeric literal parser, written by Mario Mariotta, Spring 2025 for CS 3110, Professor Qichao Dong"""

decimalAdjacencyMatrix = [[False,['1','2','3','4','5','6','7','8','9'],False,['0'],False],
                          [False,['0','1','2','3','4','5','6','7','8','9'],['_'],False,False],
                          [False,['0','1','2','3','4','5','6','7','8','9'],False,False,False],
                          [False,False,False,['0'],['_']],
                          [False,False,False,['0'],False]]

decimalAcceptanceVector = [False, True, False,True,False]


octalAdjacencyMatrix = [[False,['0'],False,False,False],
                        [False,False,['o','O'],False,False],
                        [False,False,False,['0','1','2','3','4','5','6','7'],['_']],
                        [False,False,False,['0','1','2','3','4','5','6','7'],['_']],
                        [False,False,False,['0','1','2','3','4','5','6','7'],False]]

octalAcceptanceVector = [False,False,False,True,False]


hexadecimalAdjacencyMatrix = \
    [
        [False, ['0'], False, False, False, False], 
        [False, False, ['x','X'], False, False],
        [False, False, False, ['a','b','c','d','e','f','A','B','C','D','E','F','0','1','2','3','4','5','6','7','8','9'],['_']],
        [False, False, False, ['a','b','c','d','e','f','A','B','C','D','E','F','0','1','2','3','4','5','6','7','8','9'], ['_']],
        [False, False, False, ['a','b','c','d','e','f','A','B','C','D','E','F','0','1','2','3','4','5','6','7','8','9'], False]
    ]

hexadecimalAcceptanceVector = [False, False, False, True, False]


""" 
    Explanation of states in floating point adjacency matrix:
    0 = start state
    1 = leading digit
    2 = underscore separating leading digits
    3 = convergent point leading from E/exponent to digitpart of exponent, for epsilon, branch to state 5 directly
    4 = first digit of exponent
    5 = following digits of exponent
    6 = underscore between exponent's digits
    7 = decimal with only trailing digits
    8 = convergent point for numbers with leading or trailing digits
    9 = digits trailing decimal point
    10 = underscore separating trailing digits
"""
floatingPointAdjacencyMatrix = \
    [
        [False,['0','1','2','3','4','5','6','7','8','9'],False,False,False,False,False,['.'],False,False,False], 
        [False,['0','1','2','3','4','5','6','7','8','9'],['_'],['e','E'],False,False,False,False,False,['.'],False], 
        [False,['0','1','2','3','4','5','6','7','8','9'],False,False,False,False,False,False,False,False,False], 
        [False,False,False,['-','+'],False,['0','1','2','3','4','5','6','7','8','9'],False,False,False,False,False], 
        [False,False,False,False,False,['0','1','2','3','4','5','6','7','8','9'],False,False,False,False,False], 
        [False,False,False,False,False,['0','1','2','3','4','5','6','7','8','9'],['_'],False,False,False,False], 
        [False,False,False,False,False,['0','1','2','3','4','5','6','7','8','9'],False,False,False,False,False], 
        [False,False,False,False,False,False,False,False,['0','1','2','3','4','5','6','7','8','9'],False,False], 
        [False,False,False,['e','E'],False,False,False,False,['0','1','2','3','4','5','6','7','8','9'],['0','1','2','3','4','5','6','7','8','9'],False], 
        [False,False,False,['e','E'],False,False,False,False,False,['0','1','2','3','4','5','6','7','8','9'],['_']],  
        [False,False,False,False,False,False,False,False,False,['0','1','2','3','4','5','6','7','8','9'],False]
    ] 

floatingPointAcceptanceVector = [False,False,False,False,False,True,False,False,True,True,False]


"""
    numLiteralChkr
    Name: Numeric Literal Checker
    
    Purpose: Emulates a nondeterministic finite automaton by taking in a string and checking
    whether the string could be accepted by one of the sub-automata that are based on python's
    numeric literal specifications. Each sub-NFA is represented by an adjacency matrix, and the
    function recursively delves through the string, going from state to state if there's a
    compatible transition, until it reaches the end of string and then evaluates whether the automaton
    is in an accept state using the graph's acceptance vector.

    The numeric literals that this function checks are: decimal integer, octal integer, 
    hexadecimal integer, and floating point literals.
    specification: https://docs.python.org/3/reference/lexical_analysis.html#numeric-literals
    
    Arguments: input string (str), string to be checked by automata
               index (int), the index of the character in the string to be read
               stringLength (int), the length of the input string
               state (list, size two, of ints), the current state that the automaton is, index
               0 is the index for the outer nondeterministic automaton, and then index 1 is
               the row in the sub-automaton. index 1 is the actual vertex/state in the graph
               that the automaton is in.

    returns: bool (which implies whether the string is a valid python numeric literal)
"""

# this is a three dimension matrix, since each of the matrices in this list is two dimensions
nondeterministicFiniteAutomaton = ['start',decimalAdjacencyMatrix, octalAdjacencyMatrix, hexadecimalAdjacencyMatrix, floatingPointAdjacencyMatrix]

# this is a two dimension matrix, since this is a vector of vectors.
acceptanceVector = [[False], decimalAcceptanceVector, octalAcceptanceVector, hexadecimalAcceptanceVector, floatingPointAcceptanceVector]

def numLiteralChkr(inputStr: str, index: int, stringLength: int, state: list = [0,0]) -> bool:
    adjacency = False
        
    # base case: reached end of string, check if final state transitioned to is an accept state
    if index == stringLength:
        return acceptanceVector[state[0]][state[1]]
        
    # first recursive case: beginning of string, split automaton into subautomata
    # check that we're at the beginning of the string and the state of the automaton is the start
    #   state of the whole automaton, not of sub-automaton.  
    elif index == 0 and nondeterministicFiniteAutomaton[state[0]] == 'start':
        # branch into each of the subautomata
        for i in range(1,len(nondeterministicFiniteAutomaton)):
            adjacency = numLiteralChkr(inputStr, index, stringLength, [i,0])
            # since this function is recursive, by the time the whole string has been evaluated
            # and the NFA has reached an accept state, if it has reached an accept state,
            # it would be unnecessary to check other possibilities, they are mutually exclusive
            # and we only have to know whether we've found anything acceptable at all, we don't
            # need to report what kind of numeric literal it is or at what point it was accepted
            # AND since they are mutually exclusive possibilities, none of the other sub-automata
            # would accept the string anyway
            if adjacency:
                return adjacency
        # this handles when we've exhausted all of the possible paths in the graph, and have not reached an accept state
        # since adjacency is False by default
        return adjacency
        
    # major recursive case: beginning or middle of string, subautomaton has been chosen
    else:
        # for the current state, see if there are any transitions out based on the current character being read
        for j in range(len(nondeterministicFiniteAutomaton[state[0]][state[1]])):
        # consider removing this line and breaking if adjacency becomes true
            # if adjacency:
            #     pass
            # else:
            if not nondeterministicFiniteAutomaton[state[0]][state[1]][j]:
                pass
            else: 
                if inputStr[index] in nondeterministicFiniteAutomaton[state[0]][state[1]][j]:
                    adjacency = numLiteralChkr(inputStr, index + 1, stringLength, [state[0],j])
                if adjacency:
                    break
        return adjacency


"""
    check_file_with_nfa
    Name: File Interface for Numeric Literal Checker

    Purpose: Provides a file-based interface to the numLiteralChkr function. Takes in a filename
    containing one numeric literal per line, and prints out "accept" or "reject" for each line
    depending on whether the string is a valid Python numeric literal according to the automaton.

    Arguments: filename (str), the path to the file that contains numeric literals to be checked

    Returns: None (prints results to console)
"""
def check_file_with_nfa(filename: str):
    try:
        # open the input file in read mode
        with open(filename, 'r') as file:
            lines = file.readlines()  # store all lines from the file in a list
            with open('out.txt', 'w') as output:

                # iterate through each line and its corresponding line number (1-indexed)
                for line_num, line in enumerate(lines, start=1):
                    stripped_line = line.strip()  # remove leading/trailing whitespace from each line
                    # handle the case where the line is empty
                    if not stripped_line:
                        print(f"Line {line_num}: reject (empty line)")
                        continue
                    stripped_line = stripped_line.split()
                    # lower the accept/reject expected field for comparison later in program
                    stripped_line[1] = stripped_line[1].lower()

                    # call the numeric literal checker on the current line
                    result = numLiteralChkr(stripped_line[0], 0, len(stripped_line[0]))

                    # print whether the line is accepted or rejected by the automaton
                    print(f"Line {line_num}: {'accept' if result else 'reject'}")

                    # convert result from bool to string for comparison with expected
                    result = "accept" if result else "reject"

                    output.write("Input: " + stripped_line[0] + "\tExpected: " + stripped_line[1] + "\tResult: " + result + "\t" + str((stripped_line[1] == result)) + "\n")
                  
    # handle the case where the file could not be found
    except FileNotFoundError:
        print(f"Error: File '{filename}' not found.")

    # handle any unexpected errors that occur during execution
    except Exception as e:
        print(f"An error occurred: {e}")


"""
    __main__ block

    Purpose: Prompts the user to enter a file path, and then passes that file to the NFA checker.
"""
if __name__ == "__main__":
    # prompt the user for the input file path
    input_filename = input("Enter the path to the file with numeric literals: ")

    # pass the filename to the checker interface
    check_file_with_nfa(input_filename)
