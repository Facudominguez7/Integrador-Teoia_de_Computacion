class AnalizadorSemantico:
    def __init__(self):
        self.tabla_simbolos = {}
        # Añadir conjunto para rastrear las variables usadas
        self.variables_usadas = set()

    def visitar(self, nodo):
        nombre_metodo = 'visitar_' + nodo.__class__.__name__
        visitante = getattr(self, nombre_metodo, self.visita_generica)
        return visitante(nodo)

    def visita_generica(self, nodo):
        raise Exception(f'No existe el método visitar_{nodo.__class__.__name__}')

    def visitar_Declaraciones(self, nodo):
        for declaracion in nodo.declaraciones:
            self.visitar(declaracion)

    def visitar_Asignacion(self, nodo):
        nombre_var = nodo.nombre.nombre
        valor = self.visitar(nodo.expr)
        if isinstance(valor, int):  # Asumiendo que todos los números son enteros
            self.tabla_simbolos[nombre_var] = valor  # Propagación constante
        else:
            self.tabla_simbolos[nombre_var] = None

    def visitar_Variable(self, nodo):
        nombre_var = nodo.nombre
        if nombre_var in self.tabla_simbolos:
            self.variables_usadas.add(nombre_var)  # Rastrear variables usadas
            valor = self.tabla_simbolos[nombre_var]
            if isinstance(valor, int):  # Asumiendo que todos los números son enteros
                return valor  # Retornar valor constante si está disponible
            else:
                return None
        else:
            raise Exception(f'Variable "{nombre_var}" no definida')

    def visitar_Numero(self, nodo):
        return nodo.valor

    def visitar_OperacionBinaria(self, nodo):
        valor_izquierdo = self.visitar(nodo.izquierda)
        valor_derecho = self.visitar(nodo.derecha)
        if nodo.operador == '+':
            return valor_izquierdo + valor_derecho
        elif nodo.operador == '-':
            return valor_izquierdo - valor_derecho
        elif nodo.operador == '*':
            return valor_izquierdo * valor_derecho
        elif nodo.operador == '/':
            if valor_derecho == 0:
                raise Exception('División por cero')
            return valor_izquierdo / valor_derecho
        else:
            raise Exception(f'Operador desconocido {nodo.operador}')
    
    def eliminar_codigo_muerto(self):
        # Método para eliminar código muerto después de visitar todos los nodos
        for nombre_var in list(self.tabla_simbolos.keys()):
            if nombre_var not in self.variables_usadas:
                del self.tabla_simbolos[nombre_var]  # Eliminar asignaciones no utilizadas
