import ply.lex as lex
import ply.yacc as yacc

# Analizador Léxico
tokens = [
    'NUMBER',
    'ID',
    'ASSIGN',
    'PLUS',
    'MINUS',
    'TIMES',
    'DIVIDE',
    'SEMICOLON',
    'LPAREN',
    'RPAREN'
]

t_ASSIGN = r'='
t_PLUS = r'\+'
t_MINUS = r'-'
t_TIMES = r'\*'
t_DIVIDE = r'/'
t_SEMICOLON = r';'
t_LPAREN = r'\('
t_RPAREN = r'\)'

def t_ID(t):
    r'[A-Za-z]+'
    return t

def t_NUMBER(t):
    r'\d+(\.\d+)?'
    t.value = float(t.value) if '.' in t.value else int(t.value)
    return t

def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

t_ignore = ' \t'

def t_error(t):
    print(f"Illegal character '{t.value[0]}'")
    t.lexer.skip(1)

lexer = lex.lex()

# Clases para el AST
class Nodo:
    def __init__(self, tipo, *hijos):
        self.tipo = tipo
        self.hijos = hijos

    def imprimir(self, nivel=0):
        print('  ' * nivel + self.tipo)
        for hijo in self.hijos:
            if isinstance(hijo, Nodo):
                hijo.imprimir(nivel + 1)
            else:
                print('  ' * (nivel + 1) + str(hijo))

class Id(Nodo):
    def __init__(self, valor):
        super().__init__('ID')
        self.valor = valor

class Assign(Nodo):
    def __init__(self, operador, izquierdo, derecho):
        super().__init__('ASSIGN', izquierdo, derecho)
        self.operador = operador

# Analizador Sintáctico
precedence = (
    ('left', 'PLUS', 'MINUS'),
    ('left', 'TIMES', 'DIVIDE'),
    ('right', 'ASSIGN'),
)

def p_program(p):
    '''program : statement_list'''
    p[0] = Nodo('program', *p[1])

def p_statement_list(p):
    '''statement_list : statement
                      | statement_list statement'''
    if len(p) == 2:
        p[0] = [p[1]]
    else:
        p[0] = p[1] + [p[2]]

def p_statement(p):
    '''statement : expression_statement
                 | assignment_statement'''
    p[0] = p[1]

def p_expression_statement(p):
    '''expression_statement : expression SEMICOLON'''
    p[0] = Nodo('expression_statement', p[1])

def p_assignment_statement(p):
    '''assignment_statement : ID ASSIGN expression SEMICOLON'''
    p[0] = Assign('=', Id(p[1]), p[3])

def p_expression(p):
    '''expression : term
                  | expression PLUS term
                  | expression MINUS term'''
    if len(p) == 2:
        p[0] = p[1]
    else:
        p[0] = Nodo('expression', p[1], Nodo(p[2]), p[3])

def p_term(p):
    '''term : factor
            | term TIMES factor
            | term DIVIDE factor'''
    if len(p) == 2:
        p[0] = p[1]
    else:
        p[0] = Nodo('term', p[1], Nodo(p[2]), p[3])

def p_factor(p):
    '''factor : NUMBER
              | ID
              | LPAREN expression RPAREN'''
    if len(p) == 2:
        if isinstance(p[1], int) or isinstance(p[1], float):
            p[0] = Nodo('NUMBER', p[1])
        else:
            p[0] = Id(p[1])
    else:
        p[0] = p[2]

def p_error(p):
    if p:
        print(f"Error de sintaxis en '{p.value}' en la línea {p.lineno}")
    else:
        print("Error de sintaxis en EOF")

parser = yacc.yacc()

# Función para probar el parser
def test_parser(data):
    result = parser.parse(data)
    if result:
        result.imprimir()

if __name__ == "__main__":
    data = '''
    a = 3 + 4;
    b = a * 2;
    '''
    test_parser(data)
