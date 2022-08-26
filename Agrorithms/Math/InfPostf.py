import sys
from collections import deque


# Utility function to return precedence of the given operator.
# Note that higher is the precedence, lower is its value
def prec(c):
    # Multiplication and division
    if c == '*' or c == '/':
        return 3

    # Addition and subtraction
    if c == '+' or c == '-':
        return 4

    # Bitwise AND
    if c == '&':
        return 8

    # Bitwise XOR (exclusive or)
    if c == '^':
        return 9

    # Bitwise OR (inclusive or)
    if c == '|':
        return 10

    # add more operators if needed
    return sys.maxsize  # for opening bracket '('


# Utility function to check if a given token is an operand
def isOperand(c):
    return ('a' <= c <= 'z') or ('A' <= c <= 'Z') or ('0' <= c <= '9')


# Function to convert an infix expression to a postfix expression.
# This function expects a valid infix expression
def infixToPostfix(infix):
    # base case
    if not infix or not len(infix):
        return True

    # create an empty stack for storing operators
    s = deque()

    # create a string to store the postfix expression
    postfix = ''

    # process the infix expression from left to right
    for c in infix:
        # Case 1. If the current token is an opening bracket '(', push it into
        # the stack
        if c == '(':
            s.append(c)

        # Case 2. If the current token is a closing bracket ')'
        elif c == ')':
            # pop tokens from the stack until the corresponding opening bracket '('
            # is removed. Append each operator at the end of the postfix expression
            while s[-1] != '(':
                postfix += s.pop()
            s.pop()

        # Case 3. If the current token is an operand, append it at the end of the
        # postfix expression
        elif isOperand(c):
            postfix += c

        # Case 4. If the current token is an operator
        else:
            # remove operators from the stack with higher or equal precedence
            # and append them at the end of the postfix expression
            while s and prec(c) >= prec(s[-1]):
                postfix += s.pop()

            # finally, push the current operator on top of the stack
            s.append(c)

    # append any remaining operators in the stack at the end of the postfix expression
    while s:
        postfix += s.pop()

    # return the postfix expression
    return postfix


if __name__ == '__main__':
    infix = "4^3^2"  # 'A*(B*C+D*E)+F'
    postfix = infixToPostfix(infix)
    print(postfix)


