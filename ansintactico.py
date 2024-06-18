import ply.yacc as yacc
from anlexico import tokens

class Nodo:
    pass

class Declaraciones(Nodo):
    def __init__(self, declaraciones):
        self.declaraciones = declaraciones

    def __str__(self):
        return "\n".join(str(declaracion) for declaracion in self.declaraciones)

class Asignacion(Nodo):
    def __init__(self, nombre, expr):
        self.nombre = nombre
        self.expr = expr

    def __str__(self):
        return f"{self.nombre} = {self.expr}"

class Variable(Nodo):
    def __init__(self, nombre):
        self.nombre = nombre

    def __str__(self):
        return self.nombre

class Numero(Nodo):
    def __init__(self, valor):
        self.valor = valor

    def __str__(self):
        return str(self.valor)

class OperacionBinaria(Nodo):
    def __init__(self, izquierda, operador, derecha):
        self.izquierda = izquierda
        self.operador = operador
        self.derecha = derecha

    def __str__(self):
        return f"({self.izquierda} {self.operador} {self.derecha})"


def p_declaraciones_multiples(p):
    'statements : statements statement'
    p[0] = Declaraciones(p[1].declaraciones + [p[2]])

def p_declaraciones_unica(p):
    'statements : statement'
    p[0] = Declaraciones([p[1]])

def p_declaracion_asignacion(p):
    'statement : ID ASSIGN expression SEMICOLON'
    p[0] = Asignacion(Variable(p[1]), p[3])

def p_expresion_operacion_binaria(p):
    '''expression : expression PLUS term
                  | expression MINUS term'''
    p[0] = OperacionBinaria(p[1], p[2], p[3])

def p_expresion_termino(p):
    'expression : term'
    p[0] = p[1]

def p_termino_operacion_binaria(p):
    '''term : term TIMES factor
            | term DIVIDE factor'''
    p[0] = OperacionBinaria(p[1], p[2], p[3])

def p_termino_factor(p):
    'term : factor'
    p[0] = p[1]

def p_factor_numero(p):
    'factor : NUMBER'
    p[0] = Numero(p[1])

def p_factor_id(p):
    'factor : ID'
    p[0] = Variable(p[1])

def p_factor_expresion(p):
    'factor : LPAREN expression RPAREN'
    p[0] = p[2]

def p_error(p):
    print(f"Error de sintaxis en '{p.value}'")

parser = yacc.yacc()
