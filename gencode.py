class GeneradorCodigo:
    def __init__(self):
        self.codigo = []
        self.contador_temp = 0

    def nueva_temp(self):
        self.contador_temp += 1
        return f"t{self.contador_temp}"

    def generar(self, nodo):
        nombre_metodo = 'gen_' + nodo.__class__.__name__
        generador = getattr(self, nombre_metodo, self.generico_generar)
        return generador(nodo)

    def generico_generar(self, nodo):
        raise Exception(f'No existe el método gen_{nodo.__class__.__name__}')

    def gen_Declaraciones(self, nodo):
        for declaracion in nodo.declaraciones:
            self.generar(declaracion)

    def gen_Asignacion(self, nodo):
        codigo_expr, resultado = self.generar(nodo.expr)
        self.codigo.extend(codigo_expr)
        self.codigo.append(f"{nodo.nombre.nombre} = {resultado}")

    def gen_Variable(self, nodo):
        return [], nodo.nombre

    def gen_Numero(self, nodo):
        temp = self.nueva_temp()
        return [f"{temp} = {nodo.valor}"], temp

    def gen_OperacionBinaria(self, nodo):
        codigo_izquierda, resultado_izquierda = self.generar(nodo.izquierda)
        codigo_derecha, resultado_derecha = self.generar(nodo.derecha)
        temp = self.nueva_temp()
        codigo = codigo_izquierda + codigo_derecha + [f"{temp} = {resultado_izquierda} {nodo.operador} {resultado_derecha}"]
        return codigo, temp
