class SemanticAnalyzer:
    def __init__(self):
        self.symbol_table = {}
        #añadir conjunto para rastrear las variables usadas#
        self.used_variables = set()

    def visit(self, node):
        method_name = 'visit_' + node.__class__.__name__
        visitor = getattr(self, method_name, self.generic_visit)
        return visitor(node)

    def generic_visit(self, node):
        raise Exception(f'No visit_{node.__class__.__name__} method')

    def visit_Statements(self, node):
        for statement in node.statements:
            self.visit(statement)

    def visit_Assign(self, node):
        var_name = node.name.name
        value = self.visit(node.expr)
        if isinstance(value, int):  # Asumiendo que todos los números son enteros
            self.symbol_table[var_name] = value  # Propagación constante
        else:
            self.symbol_table[var_name] = None

    def visit_Variable(self, node):
        var_name = node.name
        if var_name in self.symbol_table:
            self.used_variables.add(var_name)  # Rastrear variables usadas
            value = self.symbol_table[var_name]
            if isinstance(value, int):  # Asumiendo que todos los números son enteros
                return value  # Retornar valor constante si está disponible
            else:
                return None
        else:
            raise Exception(f'Variable "{var_name}" not defined')

    def visit_Number(self, node):
        return node.value

    def visit_BinOp(self, node):
        left_val = self.visit(node.left)
        right_val = self.visit(node.right)
        if node.op == '+':
            return left_val + right_val
        elif node.op == '-':
            return left_val - right_val
        elif node.op == '*':
            return left_val * right_val
        elif node.op == '/':
            if right_val == 0:
                raise Exception('Division by zero')
            return left_val / right_val
        else:
            raise Exception(f'Unknown operator {node.op}')
    
    def eliminate_dead_code(self):
        # Método para eliminar código muerto después de visitar todos los nodos
        for var_name in list(self.symbol_table.keys()):
            if var_name not in self.used_variables:
                del self.symbol_table[var_name]  # Eliminar asignaciones no utilizadas