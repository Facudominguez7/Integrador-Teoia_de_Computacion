from anlexico import lexer
from ansintactico import parser
from ansemantico import SemanticAnalyzer
from gencode import CodeGenerator

# Código fuente a analizar
source_code = """
a = 3 + 4;
b = a * 2;
c = b / (a - 1);
"""

# Análisis léxico
lexer.input(source_code)
print("### Análisis Léxico ###")
while True:
    tok = lexer.token()
    if not tok:
        break
    print(tok)

# Análisis sintáctico
ast = parser.parse(source_code)
print("\n### Análisis Sintáctico ###")
print(ast)

# Análisis semántico
analyzer = SemanticAnalyzer()
print("\n### Análisis Semántico ###")
try:
    analyzer.visit(ast)
    print("No semantic errors")
except Exception as e:
    print(f"Semantic Error: {e}")

# Generación de código intermedio
generator = CodeGenerator()
generator.generate(ast)
print("\n### Código Intermedio ###")
for line in generator.code:
    print(line)
