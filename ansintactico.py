import ply.yacc as yacc
from anlexico import tokens

class Node:
    pass

class Statements(Node):
    def __init__(self, statements):
        self.statements = statements

class Assign(Node):
    def __init__(self, name, expr):
        self.name = name
        self.expr = expr

class Variable(Node):
    def __init__(self, name):
        self.name = name

class Number(Node):
    def __init__(self, value):
        self.value = value

class BinOp(Node):
    def __init__(self, left, op, right):
        self.left = left
        self.op = op
        self.right = right

def p_statements_multiple(p):
    'statements : statements statement'
    p[0] = Statements(p[1].statements + [p[2]])

def p_statements_single(p):
    'statements : statement'
    p[0] = Statements([p[1]])

def p_statement_assign(p):
    'statement : ID ASSIGN expression SEMICOLON'
    p[0] = Assign(Variable(p[1]), p[3])

def p_expression_binop(p):
    '''expression : expression PLUS term
                  | expression MINUS term'''
    p[0] = BinOp(p[1], p[2], p[3])

def p_expression_term(p):
    'expression : term'
    p[0] = p[1]

def p_term_binop(p):
    '''term : term TIMES factor
            | term DIVIDE factor'''
    p[0] = BinOp(p[1], p[2], p[3])

def p_term_factor(p):
    'term : factor'
    p[0] = p[1]

def p_factor_number(p):
    'factor : NUMBER'
    p[0] = Number(p[1])

def p_factor_id(p):
    'factor : ID'
    p[0] = Variable(p[1])

def p_factor_expr(p):
    'factor : LPAREN expression RPAREN'
    p[0] = p[2]

def p_error(p):
    print(f"Syntax error at '{p.value}'")

parser = yacc.yacc()
