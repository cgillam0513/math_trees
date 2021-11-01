"""Main module."""

from enum import Enum


class TagValue(Enum):
    num = 0
    neg = 1
    add = 2
    sub = 3
    mul = 4
    div = 5
    lpar = 6


def add_func(arg1, arg2):
    return arg1 + arg2


def sub_func(arg1, arg2):
    return arg1 - arg2


def mul_func(arg1, arg2):
    return arg1 * arg2


def div_func(arg1, arg2):
    return arg1 / arg2


class OpClass:
    def __init__(self, func, op_str: str):
        self.str = op_str
        self.func = func


addClass = OpClass(add_func, '+')
subClass = OpClass(sub_func, '-')
mulClass = OpClass(mul_func, '*')
divClass = OpClass(div_func, '/')


map_tag_to_opClass = {
    TagValue.add: addClass,
    TagValue.sub: subClass,
    TagValue.mul: mulClass,
    TagValue.div: divClass
}

map_str_to_tag = {
    '+': TagValue.add,
    '-': TagValue.sub,
    '*': TagValue.mul,
    '/': TagValue.div
}


class Expr:
    def __init__(self, tag: TagValue, val, arg1, arg2):
        self.tag = tag
        self.val = val
        self.arg1 = arg1
        self.arg2 = arg2


class Number(Expr):
    def __init__(self, val):
        super().__init__(TagValue.num, val, None, None)

    def __str__(self):
        return str(self.val)

    def eval(self):
        return self.val


class Oper(Expr):
    def __init__(self, tag: TagValue, arg1: Expr, arg2: Expr):
        super().__init__(tag, None, arg1, arg2)

    def __str__(self):
        op_class = map_tag_to_opClass[self.tag]
        return str(self.arg1)+op_class.str+str(self.arg2)

    def eval(self):
        op_class = map_tag_to_opClass[self.tag]
        return op_class.func(self.arg1.eval(), self.arg2.eval())


class LParen(Expr):
    def __init__(self, arg1: Expr):
        super().__init__(TagValue.lpar, None, arg1, None)

    def __str__(self):
        return '('+str(self.arg1)+')'

    def eval(self):
        return self.arg1.eval()


def parse_num_str_from_input(input_string: str):
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
        num_string += p
        num_string, input_string = create_num_str(input_string[1:], num_string, True)
    elif '+' == p:
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


def parse_number(char_list):
    num_str, char_list = parse_num_str_from_input(char_list)
    if '.' in num_str:
        n = float(num_str)
    else:
        n = int(num_str)
    return Number(n), char_list


def parse_factor(char_list):
    c = char_list[0]
    if c.isdigit():
        expr, char_list = parse_number(char_list)
    elif '+' == c:
        # Allowing +num
        char_list.pop()
        c = char_list[0]
        if c.isdigit():
            expr, char_list = parse_number(char_list)
        else:
            raise SyntaxError
    elif '-' == c:
        # Allowing -num
        char_list.pop()
        c = char_list[0]
        if c.isdigit():
            expr, expr_string = parse_number(char_list)
            expr.val = -expr.val
        else:
            raise SyntaxError
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


def parse_term(char_list):
    expr, char_list = parse_factor(char_list)

    if char_list:
        c = char_list[0]
        while c in ['*', '/', '(']:
            if c in ['*', '/']:
                char_list.pop(0)
                expr2, char_list = parse_factor(char_list)
                expr = Oper(map_str_to_tag[c], expr, expr2)
            else:
                expr2, char_list = parse_factor(char_list)
                expr = Oper(TagValue.mul, expr, LParen(expr2))
            if char_list:
                c = char_list[0]
            else:
                break

    return expr, char_list


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


def parse_str(expr_str):
    expr_str = expr_str.replace(' ','')
    return parse_alg_expr(list(expr_str))


def eval_str_expr(expr_str):
    math_tree = parse_str(expr_str)
    val = math_tree.eval()
    s = expr_str + ' : ' + str(math_tree) + '=' + str(val)
    print(s)

parse_num_str_from_input('12324')
parse_num_str_from_input('000010003')
parse_num_str_from_input('.0000123')
parse_num_str_from_input('13124.2143')
parse_num_str_from_input('-1232')
parse_num_str_from_input('+12334')
parse_num_str_from_input('-.0000123')
parse_num_str_from_input('+.0000123')
parse_num_str_from_input('123+243')
parse_num_str_from_input('-13.13')
parse_num_str_from_input('+12.13')
# parse_number('------19.13')
# parse_number('-+++-+17.13')
# parse_number('-.0000123.')
