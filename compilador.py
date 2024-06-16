from anlexico import lexer
from ansintactico import parser
from ansemantico import analizar_programa

def compilar(data):
    # Fase de análisis léxico
    lexer.input(data)
    while True:
        tok = lexer.token()
        if not tok:
            break
        print(tok)

    # Fase de análisis sintáctico
    programa = parser.parse(data)
    if programa:
        programa.imprimir()

    # Fase de análisis semántico
    analizar_programa(programa)

if __name__ == "__main__":
    data = '''
    a = 3 + 4;
    b = a * 2;
    '''
    compilar(data)
