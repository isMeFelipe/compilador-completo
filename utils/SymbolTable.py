# symbol_table.py
class SymbolTable:
    def __init__(self):
        self.variables = {}

    def declare_variable(self, name, var_type):
        if name in self.variables:
            raise RuntimeError(f"Variable '{name}' already declared.")
        self.variables[name] = var_type

    def use_variable(self, name):
        if name not in self.variables:
            raise RuntimeError(f"Variable '{name}' not declared.")

    def get_type(self, name):
        return self.variables.get(name, None)

    def check_compatibility(self, op1, op2, operator):
        if operator == '%' and (op1 == 'float' or op2 == 'float'):
            raise RuntimeError("Operation '%' not allowed with floating point numbers.")
        if op1 == 'int' and op2 == 'float':
            op1 = 'float'
        elif op1 == 'float' and op2 == 'int':
            op2 = 'float'
        return op1, op2
