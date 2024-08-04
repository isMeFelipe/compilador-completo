class VariableAlreadyDeclaredError(Exception):
    def __init__(self, var_name):
        self.var_name = var_name
        super().__init__(f"Variável já declarada: {var_name}")

class SymbolTable:
    def __init__(self):
        self.symbols = set()  # Armazena variáveis declaradas

    def add_variable(self, var_name):
        if self.is_declared(var_name):
            raise VariableAlreadyDeclaredError(var_name)
        self.symbols.add(var_name)

    def is_declared(self, var_name):
        return var_name in self.symbols

    def __str__(self):
        return ', '.join(self.symbols)

from SimpAlgVisitor import SimpAlgVisitor
from SimpAlgParser import SimpAlgParser

class CodeGeneratorVisitor(SimpAlgVisitor):
    def __init__(self):
        self.label_count = 0
        self.symbol_table = SymbolTable()

    def get_new_label(self):
        self.label_count += 1
        return f"L{self.label_count}"

    def visitProgram(self, ctx: SimpAlgParser.ProgramContext):
        code = "#include <iostream>\nusing namespace std;\n\n"
        code += "int main() {\n"
        code += self.visit(ctx.statement_list())
        code += "\nreturn 0;\n}"
        return code

    def visitStatement_list(self, ctx: SimpAlgParser.Statement_listContext):
        code = ""
        for statement in ctx.statement():
            code += self.visit(statement) + "\n"
        return code

    def visitDeclaration(self, ctx: SimpAlgParser.DeclarationContext):
        variables = ctx.variable_list().IDENTIFIER()
        declarations = []
        
        for var in variables:
            var_name = var.getText()
            try:
                # Adiciona a variável à tabela de símbolos
                self.symbol_table.add_variable(var_name)
                # Adiciona a declaração do tipo à lista de declarações
                declarations.append(var_name)
            except VariableAlreadyDeclaredError as e:
                print(e)  # Exibe a exceção de variável já declarada, pode-se substituir por logging

        # Gera o código de declaração para as variáveis não declaradas
        if declarations:
            return f"int {', '.join(declarations)};"
        return ""

    def visitAssignment(self, ctx: SimpAlgParser.AssignmentContext):
        return f"{ctx.IDENTIFIER().getText()} = {self.visit(ctx.expression())};"

    def visitIo_statement(self, ctx: SimpAlgParser.Io_statementContext):
        values = " << ".join([self.visit(v) for v in ctx.value_list().value()])
        if ctx.READ():
            return f"cin >> {values};"
        else:
            return f"cout << {values};"

    def visitIf_statement(self, ctx: SimpAlgParser.If_statementContext):
        condition = self.visit(ctx.boolean_expression())
        then_branch = self.visit(ctx.statement_list(0))
        else_branch = self.visit(ctx.statement_list(1)) if ctx.ELSE() else ""

        true_label = self.get_new_label()
        end_label = self.get_new_label()

        code = f"if (!({condition})) goto {true_label};\n"
        code += f"{then_branch}\n"
        code += f"goto {end_label};\n"
        code += f"{true_label}:\n"
        code += f"{else_branch}\n"
        code += f"{end_label}:\n"

        return code

    def visitRepeat_statement(self, ctx: SimpAlgParser.Repeat_statementContext):
        start_label = self.get_new_label()
        end_label = self.get_new_label()

        body = self.visit(ctx.statement_list())
        condition = self.visit(ctx.boolean_expression())

        code = f"{start_label}:\n"
        code += f"{body}\n"
        code += f"if (({condition})) goto {end_label};\n"
        code += f"goto {start_label};\n"
        code += f"{end_label}:\n"

        return code

    def visitGoto_statement(self, ctx: SimpAlgParser.Goto_statementContext):
        label = ctx.IDENTIFIER().getText()
        return f"goto {label};"

    def visitLabel_declaration(self, ctx: SimpAlgParser.Label_declarationContext):
        label = ctx.LABEL_NAME().getText()
        self.labels[label] = self.current_line
        return f"{label}:"

    def visitExpression(self, ctx: SimpAlgParser.ExpressionContext):
        left = self.visit(ctx.term(0))
        if ctx.term(1):
            op = ctx.getChild(1).getText()
            right = self.visit(ctx.term(1))
            return f"{left} {op} {right}"
        return left

    def visitTerm(self, ctx: SimpAlgParser.TermContext):
        left = self.visit(ctx.factor(0))
        if ctx.factor(1):
            op = ctx.getChild(1).getText()
            right = self.visit(ctx.factor(1))
            return f"{left} {op} {right}"
        return left

    def visitFactor(self, ctx: SimpAlgParser.FactorContext):
        if ctx.primary():
            return self.visit(ctx.primary())
        if ctx.ADD() or ctx.SUB():
            return f"{ctx.getChild(0).getText()}{self.visit(ctx.primary())}"
        return self.visit(ctx.primary())

    def visitPrimary(self, ctx: SimpAlgParser.PrimaryContext):
        if ctx.NUMBER():
            return ctx.NUMBER().getText()
        if ctx.IDENTIFIER():
            return ctx.IDENTIFIER().getText()
        if ctx.LPAREN():
            return f"({self.visit(ctx.expression())})"
        return ""

    def visitBoolean_expression(self, ctx: SimpAlgParser.Boolean_expressionContext):
        terms = [self.visit(bt) for bt in ctx.boolean_term()]
        return " || ".join(terms)

    def visitBoolean_term(self, ctx: SimpAlgParser.Boolean_termContext):
        factors = [self.visit(bf) for bf in ctx.boolean_factor()]
        return " && ".join(factors)

    def visitBoolean_factor(self, ctx: SimpAlgParser.Boolean_factorContext):
        not_op = "!" if ctx.NOT() else ""
        return f"{not_op}{self.visit(ctx.boolean_primary())}"

    def visitBoolean_primary(self, ctx: SimpAlgParser.Boolean_primaryContext):
        if ctx.TRUE():
            return "true"
        if ctx.FALSE():
            return "false"
        if ctx.expression():
            op = ctx.getChild(1).getText()
            left = self.visit(ctx.expression(0))
            right = self.visit(ctx.expression(1))
            return f"({left} {op} {right})"
        return self.visit(ctx.boolean_expression())
    
def main():
    from antlr4 import FileStream, CommonTokenStream
    from SimpAlgLexer import SimpAlgLexer
    from SimpAlgParser import SimpAlgParser

    input_file = './input.txt'
    input_stream = FileStream(input_file)
    lexer = SimpAlgLexer(input_stream)
    token_stream = CommonTokenStream(lexer)
    parser = SimpAlgParser(token_stream)
    tree = parser.program()

    generator = CodeGeneratorVisitor()
    cpp_code = generator.visit(tree)

    with open('output.cpp', 'w') as f:
        f.write(cpp_code)

if __name__ == '__main__':
    main()
