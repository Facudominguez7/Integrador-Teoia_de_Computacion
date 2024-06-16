import ply.lex as lex

# Lista de tokens
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
    'RPAREN',
]

# Reglas de expresiones regulares para tokens simples
t_ASSIGN    = r'='
t_PLUS      = r'\+'
t_MINUS     = r'-'
t_TIMES     = r'\*'
t_DIVIDE    = r'/'
t_SEMICOLON = r';'
t_LPAREN    = r'\('
t_RPAREN    = r'\)'

# Regla para los identificadores (ID)
def t_ID(t):
    r'[A-Za-z]+'
    return t

# Regla para los números (NUMBER)
def t_NUMBER(t):
    r'\d+(\.\d+)?'
    t.value = float(t.value) if '.' in t.value else int(t.value)
    return t

# Regla para manejar los saltos de línea
def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

# Caracteres a ignorar (espacios y tabulaciones)
t_ignore = ' \t'

# Manejo de errores
def t_error(t):
    print(f"Illegal character '{t.value[0]}'")
    t.lexer.skip(1)

# Construir el lexer
lexer = lex.lex()

# Función para probar el lexer
def test_lexer(data):
    lexer.input(data)
    while True:
        tok = lexer.token()
        if not tok:
            break
        print(tok)

if __name__ == "__main__":
    data = '''
    a = 3 + 4;
    b = a * 2;
    '''
    test_lexer(data)
