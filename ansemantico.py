from ansintactico import parser, Nodo, Id, Assign

class AnalizadorSemantico:
    def __init__(self):
        self.tabla_simbolos = {}

    def analizar(self, nodo):
        metodo_nombre = f"analizar_{type(nodo).__name__}"
        metodo = getattr(self, metodo_nombre, self.metodo_desconocido)
        return metodo(nodo)

    def metodo_desconocido(self, nodo):
        print(f"No se cómo analizar un nodo de tipo {type(nodo).__name__}")

    def analizar_Nodo(self, nodo):
        for hijo in nodo.hijos:
            if isinstance(hijo, Nodo):
                self.analizar(hijo)

    def analizar_Id(self, nodo):
        if nodo.valor not in self.tabla_simbolos:
            raise Exception(f"Variable '{nodo.valor}' no definida.")
        return self.tabla_simbolos[nodo.valor]

    def analizar_Assign(self, nodo):
        if not isinstance(nodo.hijos[0], Id):
            raise Exception("La asignación debe ser a una variable.")
        valor = self.analizar(nodo.hijos[1])
        self.tabla_simbolos[nodo.hijos[0].valor] = valor
        return valor

def analizar_programa(programa):
    analizador = AnalizadorSemantico()
    try:
        analizador.analizar(programa)
        print("Análisis semántico completado sin errores.")
    except Exception as e:
        print(f"Error semántico: {e}")

if __name__ == "__main__":
    data = '''
    a = 3 + 4;
    b = a * 2;
    '''
    programa = parser.parse(data)
    if programa:
        programa.imprimir()
        analizar_programa(programa)
