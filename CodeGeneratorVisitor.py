import sys
from antlr4 import *
from SimpAlgLexer import SimpAlgLexer
from SimpAlgParser import SimpAlgParser
from SimpAlgListener import SimpAlgListener

class SimpAlgToCppListener(SimpAlgListener):
    def __init__(self):
        self.cpp_code = []

    def enterProgram(self, ctx:SimpAlgParser.ProgramContext):
        self.cpp_code.append("#include <iostream>")
        self.cpp_code.append("using namespace std;")
        self.cpp_code.append("int main() {")

    def exitProgram(self, ctx:SimpAlgParser.ProgramContext):
        self.cpp_code.append("return 0;")
        self.cpp_code.append("}")

    def enterDeclaration(self, ctx:SimpAlgParser.DeclarationContext):
        t_type = ctx.t_type().getText()
        if t_type == "int":
            cpp_type = "int"
        elif t_type == "float":
            cpp_type = "float"
        else:
            cpp_type = "auto"  # default type if not specified
        variables = ctx.variable_list().getText().split(',')
        for var in variables:
            self.cpp_code.append(f"{cpp_type} {var};")

    def enterAssignment(self, ctx:SimpAlgParser.AssignmentContext):
        var = ctx.IDENTIFIER().getText()
        expr = ctx.expression().getText()
        self.cpp_code.append(f"{var} = {expr};")

    def enterIo_statement(self, ctx:SimpAlgParser.Io_statementContext):
        if ctx.READ():
            variables = ctx.variable_list().getText().split(',')
            for var in variables:
                self.cpp_code.append(f"cin >> {var};")
        elif ctx.WRITE():
            values = ctx.value_list().getText().split(',')
            for value in values:
                self.cpp_code.append(f"cout << {value} << endl;")

    def enterIf_statement(self, ctx:SimpAlgParser.If_statementContext):
        condition = ctx.boolean_expression().getText()
        self.cpp_code.append(f"if ({condition}) {{")

    def exitIf_statement(self, ctx:SimpAlgParser.If_statementContext):
        if ctx.ELSE():
            self.cpp_code.append("} else {")
            self.cpp_code.append("}")
        else:
            self.cpp_code.append("}")

    def enterRepeat_statement(self, ctx:SimpAlgParser.Repeat_statementContext):
        self.cpp_code.append("do {")

    def exitRepeat_statement(self, ctx:SimpAlgParser.Repeat_statementContext):
        condition = ctx.boolean_expression().getText()
        self.cpp_code.append(f"}} while (!({condition}));")

def main():
    input_file = sys.argv[1]
    input_stream = FileStream(input_file)
    lexer = SimpAlgLexer(input_stream)
    stream = CommonTokenStream(lexer)
    parser = SimpAlgParser(stream)
    tree = parser.program()

    cpp_generator = SimpAlgToCppListener()
    walker = ParseTreeWalker()
    walker.walk(cpp_generator, tree)

    output_file = input_file.rsplit('.', 1)[0] + ".cpp"
    with open(output_file, 'w') as f:
        for line in cpp_generator.cpp_code:
            f.write(line + '\n')

    print(f"C++ code has been generated in {output_file}")

if __name__ == '__main__':
    main()
