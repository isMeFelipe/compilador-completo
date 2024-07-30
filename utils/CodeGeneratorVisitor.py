from antlr4 import *
from SimpAlgLexer import SimpAlgLexer
from SimpAlgParser import SimpAlgParser
from utils.CodeGenerator import CodeGenerator
from utils.SymbolTable import SymbolTable

class CodeGeneratorVisitor(ParseTreeVisitor):
    def __init__(self):
        self.symbol_table = SymbolTable()
        self.generator = CodeGenerator()

    def visitProgram(self, ctx:SimpAlgParser.ProgramContext):
        self.visit(ctx.statement_list())

    def visitStatement_list(self, ctx:SimpAlgParser.Statement_listContext):
        for statement in ctx.statement():
            self.visit(statement)
        # Gerar código C++ e salvar
        cpp_code = self.generator.generate_code(self.instructions)
        with open("output.cpp", "w") as f:
            f.write("#include <iostream>\nusing namespace std;\n\nint main() {\n")
            f.write(cpp_code)
            f.write("\n    return 0;\n}")
        print("Código C++ gerado e salvo em 'output.cpp'.")

    def visitDeclaration(self, ctx:SimpAlgParser.DeclarationContext):
        var_type = ctx.t_type().getText()
        for var in ctx.variable_list().IDENTIFIER():
            name = var.getText()
            self.symbol_table.declare_variable(name, var_type)
            self.generator.add_declaration(var_type, name)

    def visitAssignment(self, ctx:SimpAlgParser.AssignmentContext):
        var_name = ctx.IDENTIFIER().getText()
        value = self.visit(ctx.expression())
        self.generator.code.append(f'    {var_name} = {value};')

    def visitIo_statement(self, ctx:SimpAlgParser.Io_statementContext):
        if ctx.READ():
            vars = [var.getText() for var in ctx.variable_list().IDENTIFIER()]
            self.generator.code.append(f'    // Read variables {", ".join(vars)}')
        elif ctx.WRITE():
            values = [self.visit(val) for val in ctx.value_list().value()]
            self.generator.code.append(f'    cout << {", ".join(values)} << endl;')

    def visitIf_statement(self, ctx:SimpAlgParser.If_statementContext):
        condition = self.visit(ctx.boolean_expression())
        true_block = [self.visit(stmt) for stmt in ctx.statement_list(0).statement()]
        false_block = [self.visit(stmt) for stmt in ctx.statement_list(1).statement()] if ctx.ELSE() else []
        self.generator.generate_if_code(condition, true_block, false_block)

    def visitRepeat_statement(self, ctx:SimpAlgParser.Repeat_statementContext):
        statements = [self.visit(stmt) for stmt in ctx.statement_list().statement()]
        condition = self.visit(ctx.boolean_expression())
        self.generator.code.append(f'    // Repeat block until ({condition})')

    def visitExpression(self, ctx:SimpAlgParser.ExpressionContext):
        return self.visit(ctx.term())

    def visitTerm(self, ctx:SimpAlgParser.TermContext):
        result = self.visit(ctx.factor(0))
        for op, factor in zip(ctx.ADD(), ctx.factor()[1:]):
            result = f'({result} {op.getText()} {self.visit(factor)})'
        return result

    def visitFactor(self, ctx:SimpAlgParser.FactorContext):
        return self.visit(ctx.primary())

    def visitPrimary(self, ctx:SimpAlgParser.PrimaryContext):
        if ctx.NUMBER():
            return ctx.NUMBER().getText()
        elif ctx.IDENTIFIER():
            return ctx.IDENTIFIER().getText()
        elif ctx.LPAREN():
            return f'({self.visit(ctx.expression())})'

    def visitBoolean_expression(self, ctx:SimpAlgParser.Boolean_expressionContext):
        return ' and '.join(self.visit(term) for term in ctx.boolean_term())

    def visitBoolean_term(self, ctx:SimpAlgParser.Boolean_termContext):
        return ' or '.join(self.visit(factor) for factor in ctx.boolean_factor())

    def visitBoolean_factor(self, ctx:SimpAlgParser.Boolean_factorContext):
        if ctx.NOT():
            return f'not {self.visit(ctx.boolean_primary())}'
        return self.visit(ctx.boolean_primary())

    def visitBoolean_primary(self, ctx:SimpAlgParser.Boolean_primaryContext):
        if ctx.TRUE():
            return 'true'
        elif ctx.FALSE():
            return 'false'
        elif ctx.expression():
            left = self.visit(ctx.expression(0))
            op = ctx.getChild(1).getText()
            right = self.visit(ctx.expression(1))
            return f'({left} {op} {right})'
        elif ctx.LPAREN():
            return f'({self.visit(ctx.boolean_expression())})'

def main(input_file):
    lexer = SimpAlgLexer(FileStream(input_file))
    stream = CommonTokenStream(lexer)
    parser = SimpAlgParser(stream)
    tree = parser.program()

    visitor = CodeGeneratorVisitor()
    visitor.visit(tree)

if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1:
        main(sys.argv[1])
    else:
        print("Usage: python code_generator_visitor.py <input_file>")
