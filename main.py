# main.py
from utils.SymbolTable import SymbolTable
from utils.CodeGenerator import CodeGenerator

def main():
    symbol_table = SymbolTable()
    
    symbol_table.declare_variable('a', 'int')
    symbol_table.declare_variable('b', 'int')
    symbol_table.declare_variable('result', 'int')
    
    symbol_table.use_variable('a')
    symbol_table.use_variable('b')
    symbol_table.use_variable('result')

    instructions = [
        {'type': 'assignment', 'variable': 'a', 'value': '0'},
        {'type': 'assignment', 'variable': 'b', 'value': '5'},
        {'type': 'operation', 'result_var': 'result', 'left_var': 'a', 'right_var': 'b'},
        {'type': 'if', 'condition': 'result > 10', 
         'true_block': [
            'cout << "Result is greater than 10" << endl;'
         ],
         'false_block': [
            'cout << "Result is 10 or less" << endl;'
         ]},
        {'type': 'print', 'value': 'result'}
    ]

    generator = CodeGenerator()
    cpp_code = generator.generate_code(instructions)

    # Salvar o código C++ em um arquivo
    with open("output.cpp", "w") as f:
        f.write("#include <iostream>\nusing namespace std;\n\nint main() {\n")
        f.write(cpp_code)
        f.write("\n    return 0;\n}")

    print("Código C++ gerado e salvo em 'output.cpp'.")

if __name__ == "__main__":
    main()
