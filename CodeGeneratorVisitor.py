from SimpAlgVisitor import SimpAlgVisitor
from SimpAlgParser import SimpAlgParser
import argparse
from antlr4 import FileStream, CommonTokenStream
from SimpAlgLexer import SimpAlgLexer

class VariableAlreadyDeclaredError(Exception):
    def __init__(self, var_name):
        super().__init__(f"Variável já declarada: {var_name}")

class VariableNotDeclaredError(Exception):
    def __init__(self, var_name):
        super().__init__(f"Variável não declarada: {var_name}")

class VariableNotInitializedError(Exception):
    def __init__(self, var_name):
        super().__init__(f"Variável não inicializada: {var_name}")

class TypeError(Exception):
    def __init__(self, message):
        super().__init__(message)

class InvalidOperationError(Exception):
    def __init__(self, message):
        super().__init__(message)

class SymbolTable:
    def __init__(self):
        self.symbols = {}  # Armazena variáveis declaradas e seus tipos
        self.initialized = set()  # Armazena variáveis inicializadas

    def add_variable(self, var_name, var_type):
        if var_name in self.symbols:
            raise VariableAlreadyDeclaredError(var_name)
        self.symbols[var_name] = var_type

    def is_declared(self, var_name):
        return var_name in self.symbols

    def is_initialized(self, var_name):
        return var_name in self.initialized

    def initialize_variable(self, var_name):
        if self.is_declared(var_name):
            self.initialized.add(var_name)
        else:
            raise VariableNotDeclaredError(var_name)

    def get_type(self, var_name):
        return self.symbols.get(var_name, None)

    def __str__(self):
        return ', '.join([f"{name}: {typ}" for name, typ in self.symbols.items()])


class CodeGeneratorVisitor(SimpAlgVisitor):
    def __init__(self):
        self.label_count = 0
        self.symbol_table = SymbolTable()  # Inicializa a tabela de símbolos

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
        var_type = ctx.t_type().getText()  # Obtém o tipo da variável (int ou float)
        for var in ctx.variable_list().IDENTIFIER():
            var_name = var.getText()
            try:
                self.symbol_table.add_variable(var_name, var_type)
            except VariableAlreadyDeclaredError as e:
                raise e
        return f"{var_type} {', '.join([var.getText() for var in ctx.variable_list().IDENTIFIER()])};"

    def visitAssignment(self, ctx: SimpAlgParser.AssignmentContext):
        var_name = ctx.IDENTIFIER().getText()
        if not self.symbol_table.is_declared(var_name):
            raise VariableNotDeclaredError(var_name)
        
        # Marcar variável como inicializada
        self.symbol_table.initialize_variable(var_name)

        expression_code, expression_type = self.visit(ctx.expression())
        var_type = self.symbol_table.get_type(var_name)

        if var_type == 'int' and expression_type == 'float':
            raise TypeError(f"Erro de tipo: Não é possível atribuir um valor decimal a uma variável do tipo 'int'.")

        if var_type != expression_type:
            if var_type == 'int' and expression_type == 'float':
                expression_code = f"(int){expression_code}"
            elif var_type == 'float' and expression_type == 'int':
                expression_code = f"(float){expression_code}"
        
        return f"{var_name} = {expression_code};"

    def visitIo_statement(self, ctx: SimpAlgParser.Io_statementContext):
        if ctx.READ():
            variables = [v.getText() for v in ctx.value_list().value()]
            for var in variables:
                if not self.symbol_table.is_declared(var):
                    raise VariableNotDeclaredError(var)
                if not self.symbol_table.is_initialized(var):
                    self.symbol_table.initialize_variable(var)
            return f"cin >> {', '.join(variables)};"
        elif ctx.WRITE():
            values = []
            for value in ctx.value_list().value():
                visit_result = self.visit(value)
                if visit_result is None:
                    raise ValueError(f"Unexpected None value when visiting: {value.getText()}")
                values.append(visit_result[0])
            
            output_parts = []
            for value in values:
                if value.startswith('"') and value.endswith('"'):
                    output_parts.append('<< ' + value)
                else:
                    output_parts.append(f"<< {value}")
            return 'cout' + ' '.join(output_parts) + ' << endl;'


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
        code += f"if {condition} goto {end_label};\n"
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
        left_code, left_type = self.visit(ctx.term(0))
        if ctx.term(1):
            op = ctx.getChild(1).getText()
            right_code, right_type = self.visit(ctx.term(1))

            # Verificação para a operação de módulo
            if op == "%" and (left_type == 'float' or right_type == 'float'):
                raise InvalidOperationError("Não é possível realizar a operação de módulo com variáveis do tipo 'float'.")

            # Verificar se variáveis foram inicializadas
            if not (left_type == 'int' or left_type == 'float'):
                raise VariableNotInitializedError("Uma ou mais variáveis usadas na expressão não foram inicializadas.")

            # Conversão de tipos
            if left_type != right_type:
                if left_type == 'int' and right_type == 'float':
                    left_code = f"(float){left_code}"
                elif left_type == 'float' and right_type == 'int':
                    right_code = f"(float){right_code}"
                expr_type = 'float'
            else:
                expr_type = left_type
            
            return f"{left_code} {op} {right_code}", expr_type
        
        return left_code, left_type

    def visitTerm(self, ctx: SimpAlgParser.TermContext):
        left_code, left_type = self.visit(ctx.factor(0))
        if ctx.factor(1):
            op = ctx.getChild(1).getText()
            right_code, right_type = self.visit(ctx.factor(1))

            # Verificação para a operação de módulo
            if op == "%" and (left_type == 'float' or right_type == 'float'):
                raise InvalidOperationError("Não é possível realizar a operação de módulo com variáveis do tipo 'float'.")

            # Verificar se variáveis foram inicializadas
            if not (left_type == 'int' or left_type == 'float'):
                raise VariableNotInitializedError("Uma ou mais variáveis usadas na expressão não foram inicializadas.")

            # Conversão de tipos
            if left_type != right_type:
                if left_type == 'int' and right_type == 'float':
                    left_code = f"(float){left_code}"
                elif left_type == 'float' and right_type == 'int':
                    right_code = f"(float){right_code}"
                expr_type = 'float'
            else:
                expr_type = left_type

            return f"{left_code} {op} {right_code}", expr_type
        
        return left_code, left_type

    def visitFactor(self, ctx: SimpAlgParser.FactorContext):
        if ctx.primary():
            return self.visit(ctx.primary())
        if ctx.ADD() or ctx.SUB():
            code, typ = self.visit(ctx.primary())
            return f"{ctx.getChild(0).getText()}{code}", typ
        return self.visit(ctx.primary())

    def visitPrimary(self, ctx: SimpAlgParser.PrimaryContext):
        if ctx.NUMBER():
            number = ctx.NUMBER().getText()
            if '.' in number:
                return number, 'float'
            return number, 'int'
        if ctx.IDENTIFIER():
            var_name = ctx.IDENTIFIER().getText()
            if not self.symbol_table.is_declared(var_name):
                raise VariableNotDeclaredError(var_name)
            if not self.symbol_table.is_initialized(var_name):
                raise VariableNotInitializedError(var_name)
            return var_name, self.symbol_table.get_type(var_name)
        if ctx.LPAREN():
            return f"({self.visit(ctx.expression())})", self.visit(ctx.expression())[1]
        if ctx.STRING():
            return ctx.STRING().getText(), 'string'
        return ""
    
    def visitValue(self, ctx: SimpAlgParser.ValueContext):
        if ctx.STRING():
            return ctx.STRING().getText(), 'string'
        return self.visitChildren(ctx)


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
            left_code, left_type = self.visit(ctx.expression(0))
            right_code, right_type = self.visit(ctx.expression(1))
            # Conversão de tipos
            if left_type != right_type:
                if left_type == 'int' and right_type == 'float':
                    left_code = f"(float){left_code}"
                elif left_type == 'float' and right_type == 'int':
                    right_code = f"(float){right_code}"
            return f"({left_code} {op} {right_code})"
        return self.visit(ctx.boolean_expression())

def main():
    parser = argparse.ArgumentParser(description="Gerador de código em C++ a partir de código SimpAlg.")
    parser.add_argument("input_file", help="Caminho para o arquivo de entrada contendo o código SimpAlg.")
    parser.add_argument("output_file", help="Caminho para o arquivo de saída para armazenar o código C++ gerado.")
    
    args = parser.parse_args()

    input_stream = FileStream(args.input_file)
    lexer = SimpAlgLexer(input_stream)
    token_stream = CommonTokenStream(lexer)
    parser = SimpAlgParser(token_stream)
    tree = parser.program()

    visitor = CodeGeneratorVisitor()
    cpp_code = visitor.visit(tree)

    with open(args.output_file, 'w') as output_file:
        output_file.write(cpp_code)

if __name__ == "__main__":
    main()
