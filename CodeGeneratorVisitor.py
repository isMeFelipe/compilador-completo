import sys
from antlr4 import *
from SimpAlgLexer import SimpAlgLexer
from SimpAlgParser import SimpAlgParser
from SimpAlgListener import SimpAlgListener

class SimpAlgToCppListener(SimpAlgListener):
    def __init__(self):
        self.cpp_code = []
        self.indent_level = 0

    def add_line(self, line):
        self.cpp_code.append('\t' * self.indent_level + line)

    def enterProgram(self, ctx:SimpAlgParser.ProgramContext):
        self.cpp_code.append("#include <iostream>")
        self.cpp_code.append("using namespace std;")
        self.add_line("int main() {")
        self.indent_level += 1

    def exitProgram(self, ctx:SimpAlgParser.ProgramContext):
        self.indent_level -= 1
        self.add_line("return 0;")
        self.add_line("}")

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
            self.add_line(f"{cpp_type} {var};")

    def enterAssignment(self, ctx:SimpAlgParser.AssignmentContext):
        var = ctx.IDENTIFIER().getText()
        expr = ctx.expression().getText()
        self.add_line(f"{var} = {expr};")

    def enterIo_statement(self, ctx:SimpAlgParser.Io_statementContext):
        if ctx.READ():
            variables = ctx.variable_list().getText().split(',')
            for var in variables:
                self.add_line(f"cin >> {var};")
        elif ctx.WRITE():
            values = ctx.value_list().getText().split(',')
            for value in values:
                self.add_line(f"cout << {value} << endl;")

    def enterIf_statement(self, ctx:SimpAlgParser.If_statementContext):
        condition = ctx.boolean_expression().getText()
        self.add_line(f"if ({condition}) {{")
        self.indent_level += 1

    def exitIf_statement(self, ctx:SimpAlgParser.If_statementContext):
        self.indent_level -= 1
        if ctx.ELSE():
            self.add_line("} else {")
            self.indent_level += 1
            self.indent_level -= 1
        self.add_line("}")

    def enterRepeat_statement(self, ctx:SimpAlgParser.Repeat_statementContext):
        self.add_line("do {")
        self.indent_level += 1

    def exitRepeat_statement(self, ctx:SimpAlgParser.Repeat_statementContext):
        self.indent_level -= 1
        condition = ctx.boolean_expression().getText()
        self.add_line(f"}} while (!({condition}));")

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

    output_file = "output.cpp"
    with open(output_file, 'w') as f:
        for line in cpp_generator.cpp_code:
            f.write(line + '\n')

    print(f"C++ code has been generated in {output_file}")

if __name__ == '__main__':
    main()
