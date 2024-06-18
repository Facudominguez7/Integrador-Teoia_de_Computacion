from anlexico import lexer
from ansintactico import parser
from ansemantico import AnalizadorSemantico
from gencode import GeneradorCodigo

# Código fuente a analizar
codigo_entrada = """
a = 3 + 4;
b = a * 2;
c = b / (a - 1);
"""

# Análisis léxico
lexer.input(codigo_entrada)
print("### Análisis Léxico ###")
while True:
    tok = lexer.token()
    if not tok:
        break
    print(tok)

# Análisis sintáctico
ast = parser.parse(codigo_entrada)
print("\n### Análisis Sintáctico ###")
print(ast)

# Análisis semántico
anSemantico = AnalizadorSemantico()
print("\n### Análisis Semántico ###")
try:
    anSemantico.visitar(ast)
    print("Sin errores semánticos")
except Exception as e:
    print(f"Error Semántico: {e}")

# Generación de código intermedio
generador = GeneradorCodigo()
generador.generar(ast)
print("\n### Código Intermedio ###")
for linea in generador.codigo:
    print(linea)
