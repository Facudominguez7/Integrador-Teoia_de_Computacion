class CodeGenerator:
    def __init__(self):
        self.code = []
        self.temp_count = 0

    def new_temp(self):
        self.temp_count += 1
        return f"t{self.temp_count}"

    def generate(self, node):
        method_name = 'gen_' + node.__class__.__name__
        generator = getattr(self, method_name, self.generic_generate)
        return generator(node)

    def generic_generate(self, node):
        raise Exception(f'No gen_{node.__class__.__name__} method')

    def gen_Statements(self, node):
        for statement in node.statements:
            self.generate(statement)

    def gen_Assign(self, node):
        expr_code, result = self.generate(node.expr)
        self.code.extend(expr_code)
        self.code.append(f"{node.name.name} = {result}")

    def gen_Variable(self, node):
        return [], node.name

    def gen_Number(self, node):
        temp = self.new_temp()
        return [f"{temp} = {node.value}"], temp

    def gen_BinOp(self, node):
        left_code, left_result = self.generate(node.left)
        right_code, right_result = self.generate(node.right)
        temp = self.new_temp()
        code = left_code + right_code + [f"{temp} = {left_result} {node.op} {right_result}"]
        return code, temp
