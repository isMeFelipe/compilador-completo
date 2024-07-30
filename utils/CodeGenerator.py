# code_generator.py
class CodeGenerator:
    def __init__(self):
        self.declarations = set()  # Conjunto para armazenar declarações de variáveis
        self.code = []             # Lista para armazenar as linhas de código C++
        self.label_counter = 0     # Contador para gerar rótulos únicos

    def add_declaration(self, var_type, var_name):
        if var_name not in self.declarations:
            self.declarations.add(var_name)
            self.code.append(f'    {var_type} {var_name};')

    def generate_if_code(self, condition, true_block, false_block):
        # Gerar rótulos únicos para if
        label_true = f"IF_TRUE_{self.label_counter}"
        label_end = f"IF_END_{self.label_counter}"
        label_false = f"IF_FALSE_{self.label_counter}"
        self.label_counter += 1

        # Código C++ para o bloco if
        self.code.append(f'    if ({condition}) {{')
        self.code.extend(f'    {line}' for line in true_block)
        self.code.append(f'    }}')
        self.code.append(f'    else {{')
        self.code.extend(f'    {line}' for line in false_block)
        self.code.append(f'    }}')
        self.code.append(f'    goto {label_end};')  # Salta para o fim do bloco if
        self.code.append(f'{label_true}:')  # Rótulo para o bloco verdadeiro
        self.code.append(f'    goto {label_end};')  # Salta para o fim do bloco
        self.code.append(f'{label_false}:')  # Rótulo para o bloco falso
        self.code.append(f'{label_end}:')  # Rótulo de fim do bloco if

    def generate_code(self, instructions):
        # Adicionar declarações de variáveis
        for instr in instructions:
            if instr['type'] == 'assignment':
                self.add_declaration('int', instr["variable"])
            elif instr['type'] == 'operation':
                self.add_declaration('int', instr["result_var"])
                self.add_declaration('int', instr["left_var"])
                self.add_declaration('int', instr["right_var"])

        # Gerar as instruções de código
        for instr in instructions:
            if instr['type'] == 'assignment':
                self.code.append(f'    {instr["variable"]} = {instr["value"]};')
            elif instr['type'] == 'operation':
                self.code.append(f'    {instr["result_var"]} = {instr["left_var"]} + {instr["right_var"]};')
            elif instr['type'] == 'print':
                self.code.append(f'    cout << {instr["value"]} << endl;')
            elif instr['type'] == 'if':
                self.generate_if_code(instr["condition"], instr["true_block"], instr.get("false_block", []))

        return '\n'.join(self.code)
