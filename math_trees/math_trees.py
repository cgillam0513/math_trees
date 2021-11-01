"""Main module."""

# Pearson Coding Challenge
# Author: Christopher Gillam
# Date: 10/01/2021

from enum import Enum

# Tags will be used to tokenize numbers and operators
# left parenthesis will be treated like a 1 argument function.  There is no need to tokenize the right parenthesis
class TagValue(Enum):
    num = 0
    neg = 1
    add = 2
    sub = 3
    mul = 4
    div = 5
    lpar = 6


# Mapping strings to the tags
map_str_to_tag = {
    '+': TagValue.add,
    '-': TagValue.sub,
    '*': TagValue.mul,
    '/': TagValue.div
}


# The following function operator definitions may not be necessary for this project.  However, this coding style allows
# for customization of functions.
def add_func(arg1, arg2):
    return arg1 + arg2


def sub_func(arg1, arg2):
    return arg1 - arg2


def mul_func(arg1, arg2):
    return arg1 * arg2


def div_func(arg1, arg2):
    return arg1 / arg2


# The OpClass (operator class) stores information about the operator tokens.  Future information could be given here
# such as operator precedence or number of arguments for a function
class OpClass:
    def __init__(self, func, op_str: str):
        self.str = op_str
        self.func = func


# Creating the operator classes
addClass = OpClass(add_func, '+')
subClass = OpClass(sub_func, '-')
mulClass = OpClass(mul_func, '*')
divClass = OpClass(div_func, '/')


# Mapping tags to the operator classes
map_tag_to_opClass = {
    TagValue.add: addClass,
    TagValue.sub: subClass,
    TagValue.mul: mulClass,
    TagValue.div: divClass
}


# Expr is the tree/node structure for creating an expression.  Expr can be a number or an algebraic expression.
class Expr:
    def __init__(self, tag: TagValue, val, arg1, arg2):
        self.tag = tag
        self.val = val
        self.arg1 = arg1
        self.arg2 = arg2
        # This class could be abstracted more.  For example, instead of having 2 arguments, this class could just have
        # an array of arguments.


# Number is a type of expression (Expr) with no arguments (arg1, arg2).
class Number(Expr):
    def __init__(self, val):
        super().__init__(TagValue.num, val, None, None)

    def __str__(self):
        return str(self.val)

    def eval(self):
        return self.val


# Oper is a type of expression with an operator as a tag and no value (val).
class Oper(Expr):
    def __init__(self, tag: TagValue, arg1: Expr, arg2: Expr):
        super().__init__(tag, None, arg1, arg2)

    def __str__(self):
        op_class = map_tag_to_opClass[self.tag]
        return str(self.arg1)+op_class.str+str(self.arg2)

    def eval(self):
        op_class = map_tag_to_opClass[self.tag]
        return op_class.func(self.arg1.eval(), self.arg2.eval())


# LParen is a type of Expr with 1 argument and no value.  LParen can be viewed as a 1 argument operator
class LParen(Expr):
    def __init__(self, arg1: Expr):
        super().__init__(TagValue.lpar, None, arg1, None)

    def __str__(self):
        return '('+str(self.arg1)+')'

    def eval(self):
        return self.arg1.eval()


# This routine takes a list of characters and parses a number string
# Input: input_string is a list of characters
# Output: Returns 2 values num_str, input_string.
#         num_str is a string which represents a number
#         input_str is the remaining list from the input after the num_str has been removed
def parse_num_str_from_input(input_string):
    def create_num_str(input_str, num_str, b_did_see_dec):
        indx = -1
        for c in input_str:
            indx += 1
            if c.isdigit():
                num_str += c
            elif c == '.':
                if b_did_see_dec:
                    raise SyntaxError
                else:
                    b_did_see_dec = True
                    num_str += c
            else:
                indx -= 1
                break

        return num_str, input_str[indx + 1:]

    p = input_string[0]
    num_string = ""
    if '.' == p:
        # .2 is a valid number
        num_string += p
        num_string, input_string = create_num_str(input_string[1:], num_string, True)
    elif '+' == p:
        # +123 is a valid number
        if input_string[1] in ['+', '-']:
            raise SyntaxError
        num_string, input_string = parse_num_str_from_input(input_string[1:])
    elif '-' == p:
        if input_string[1] in ['+', '-']:
            raise SyntaxError
        num_string, input_string = parse_num_str_from_input(input_string[1:])
        num_string = '-' + num_string
    else:
        num_string, input_string = create_num_str(input_string, num_string, False)

    return num_string, input_string


# This routine parses and creates a Number from a list of characters
# Input: char_list - a list of characters
# Output: num, char_list
#         num - is a Number which represents the parsed number
#         char_list - the remaining list of characters after parsing the number
def parse_number(char_list):
    num_str, char_list = parse_num_str_from_input(char_list)
    if '.' in num_str:
        n = float(num_str)
    else:
        n = int(num_str)
    return Number(n), char_list


# This routine parses and creates an Expr from a list of characters.  This routines is looking for factors, i.e. numbers
# or expressions wrapped in parenthesis.
# Input: char_list - a list of characters
# Output: expr, char_list
#         expr - is an Expr which represents the parsed factor
#         char_list - the remaining list of characters after parsing the factor
def parse_factor(char_list):
    c = char_list[0]
    if c.isdigit() or c in ['+', '-', '.']:
        expr, char_list = parse_number(char_list)
    elif '(' == c:
        char_list.pop(0)
        cntr = 1
        new_list = []
        while char_list:
            c = char_list.pop(0)
            if '(' == c:
                cntr += 1
            elif ')' == c:
                cntr -= 1

            if 0 == cntr:
                expr = parse_alg_expr(new_list)
                expr = LParen(expr)
                break
            else:
                new_list.append(c)
        if 0 != cntr:
            raise SyntaxError
    else:
        raise SyntaxError

    return expr, char_list


# This routine parses and creates an Expr from a list of characters.  This routines is looking for terms, i.e. numbers
# expressions wrapped in parenthesis, or products of expressions
# Input: char_list - a list of characters
# Output: expr, char_list
#         expr - is an Expr which represents the parsed term
#         char_list - the remaining list of characters after parsing the term
def parse_term(char_list):
    expr, char_list = parse_factor(char_list)

    if char_list:
        c = char_list[0]
        while c in ['*', '/', '(']:
            if c in ['*', '/']:
                char_list.pop(0)
                tag = map_str_to_tag[c]
            else:
                # Have implicit multiplication
                tag = TagValue.mul

            expr2, char_list = parse_factor(char_list)
            expr = Oper(tag, expr, expr2)

            if char_list:
                c = char_list[0]
            else:
                break

    return expr, char_list


# This routine parses and creates an Expr from a list of characters.
# Input: char_list - a list of characters
# Output: expr - is an Expr which represents the parsed algebraic expression
def parse_alg_expr(char_list):
    expr, char_list = parse_term(char_list)
    if char_list:
        c = char_list[0]
        while c in ['+', '-']:
            char_list.pop(0)
            expr2, char_list = parse_term(char_list)
            expr = Oper(map_str_to_tag[c], expr, expr2)
            if char_list:
                c = char_list[0]
            else:
                break

    if char_list:
        raise SyntaxError

    return expr


# Creates an Expr tree from a string
# Input - expr_str - a string representing an algebraic expression
# Output - returns an Expr which is the math tree
def parse_str(expr_str):
    expr_str = expr_str.replace(' ', '')
    return parse_alg_expr(list(expr_str))


# Evaluates a string which represent a math expression and prints the result
# Input - expr_str - a string which represents a math expression
# Prints result on screen
def eval_str_expr(expr_str):
    math_tree = parse_str(expr_str)
    val = math_tree.eval()
    s = expr_str + ' : ' + str(math_tree) + '=' + str(val)
    print(s)

