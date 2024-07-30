# Generated from SimpAlg.g4 by ANTLR 4.9.2
from antlr4 import *
if __name__ is not None and "." in __name__:
    from .SimpAlgParser import SimpAlgParser
else:
    from SimpAlgParser import SimpAlgParser

# This class defines a complete listener for a parse tree produced by SimpAlgParser.
class SimpAlgListener(ParseTreeListener):

    # Enter a parse tree produced by SimpAlgParser#program.
    def enterProgram(self, ctx:SimpAlgParser.ProgramContext):
        pass

    # Exit a parse tree produced by SimpAlgParser#program.
    def exitProgram(self, ctx:SimpAlgParser.ProgramContext):
        pass


    # Enter a parse tree produced by SimpAlgParser#statement_list.
    def enterStatement_list(self, ctx:SimpAlgParser.Statement_listContext):
        pass

    # Exit a parse tree produced by SimpAlgParser#statement_list.
    def exitStatement_list(self, ctx:SimpAlgParser.Statement_listContext):
        pass


    # Enter a parse tree produced by SimpAlgParser#statement.
    def enterStatement(self, ctx:SimpAlgParser.StatementContext):
        pass

    # Exit a parse tree produced by SimpAlgParser#statement.
    def exitStatement(self, ctx:SimpAlgParser.StatementContext):
        pass


    # Enter a parse tree produced by SimpAlgParser#declaration.
    def enterDeclaration(self, ctx:SimpAlgParser.DeclarationContext):
        pass

    # Exit a parse tree produced by SimpAlgParser#declaration.
    def exitDeclaration(self, ctx:SimpAlgParser.DeclarationContext):
        pass


    # Enter a parse tree produced by SimpAlgParser#variable_list.
    def enterVariable_list(self, ctx:SimpAlgParser.Variable_listContext):
        pass

    # Exit a parse tree produced by SimpAlgParser#variable_list.
    def exitVariable_list(self, ctx:SimpAlgParser.Variable_listContext):
        pass


    # Enter a parse tree produced by SimpAlgParser#t_type.
    def enterT_type(self, ctx:SimpAlgParser.T_typeContext):
        pass

    # Exit a parse tree produced by SimpAlgParser#t_type.
    def exitT_type(self, ctx:SimpAlgParser.T_typeContext):
        pass


    # Enter a parse tree produced by SimpAlgParser#assignment.
    def enterAssignment(self, ctx:SimpAlgParser.AssignmentContext):
        pass

    # Exit a parse tree produced by SimpAlgParser#assignment.
    def exitAssignment(self, ctx:SimpAlgParser.AssignmentContext):
        pass


    # Enter a parse tree produced by SimpAlgParser#io_statement.
    def enterIo_statement(self, ctx:SimpAlgParser.Io_statementContext):
        pass

    # Exit a parse tree produced by SimpAlgParser#io_statement.
    def exitIo_statement(self, ctx:SimpAlgParser.Io_statementContext):
        pass


    # Enter a parse tree produced by SimpAlgParser#value_list.
    def enterValue_list(self, ctx:SimpAlgParser.Value_listContext):
        pass

    # Exit a parse tree produced by SimpAlgParser#value_list.
    def exitValue_list(self, ctx:SimpAlgParser.Value_listContext):
        pass


    # Enter a parse tree produced by SimpAlgParser#value.
    def enterValue(self, ctx:SimpAlgParser.ValueContext):
        pass

    # Exit a parse tree produced by SimpAlgParser#value.
    def exitValue(self, ctx:SimpAlgParser.ValueContext):
        pass


    # Enter a parse tree produced by SimpAlgParser#if_statement.
    def enterIf_statement(self, ctx:SimpAlgParser.If_statementContext):
        pass

    # Exit a parse tree produced by SimpAlgParser#if_statement.
    def exitIf_statement(self, ctx:SimpAlgParser.If_statementContext):
        pass


    # Enter a parse tree produced by SimpAlgParser#repeat_statement.
    def enterRepeat_statement(self, ctx:SimpAlgParser.Repeat_statementContext):
        pass

    # Exit a parse tree produced by SimpAlgParser#repeat_statement.
    def exitRepeat_statement(self, ctx:SimpAlgParser.Repeat_statementContext):
        pass


    # Enter a parse tree produced by SimpAlgParser#expression.
    def enterExpression(self, ctx:SimpAlgParser.ExpressionContext):
        pass

    # Exit a parse tree produced by SimpAlgParser#expression.
    def exitExpression(self, ctx:SimpAlgParser.ExpressionContext):
        pass


    # Enter a parse tree produced by SimpAlgParser#term.
    def enterTerm(self, ctx:SimpAlgParser.TermContext):
        pass

    # Exit a parse tree produced by SimpAlgParser#term.
    def exitTerm(self, ctx:SimpAlgParser.TermContext):
        pass


    # Enter a parse tree produced by SimpAlgParser#factor.
    def enterFactor(self, ctx:SimpAlgParser.FactorContext):
        pass

    # Exit a parse tree produced by SimpAlgParser#factor.
    def exitFactor(self, ctx:SimpAlgParser.FactorContext):
        pass


    # Enter a parse tree produced by SimpAlgParser#primary.
    def enterPrimary(self, ctx:SimpAlgParser.PrimaryContext):
        pass

    # Exit a parse tree produced by SimpAlgParser#primary.
    def exitPrimary(self, ctx:SimpAlgParser.PrimaryContext):
        pass


    # Enter a parse tree produced by SimpAlgParser#boolean_expression.
    def enterBoolean_expression(self, ctx:SimpAlgParser.Boolean_expressionContext):
        pass

    # Exit a parse tree produced by SimpAlgParser#boolean_expression.
    def exitBoolean_expression(self, ctx:SimpAlgParser.Boolean_expressionContext):
        pass


    # Enter a parse tree produced by SimpAlgParser#boolean_term.
    def enterBoolean_term(self, ctx:SimpAlgParser.Boolean_termContext):
        pass

    # Exit a parse tree produced by SimpAlgParser#boolean_term.
    def exitBoolean_term(self, ctx:SimpAlgParser.Boolean_termContext):
        pass


    # Enter a parse tree produced by SimpAlgParser#boolean_factor.
    def enterBoolean_factor(self, ctx:SimpAlgParser.Boolean_factorContext):
        pass

    # Exit a parse tree produced by SimpAlgParser#boolean_factor.
    def exitBoolean_factor(self, ctx:SimpAlgParser.Boolean_factorContext):
        pass


    # Enter a parse tree produced by SimpAlgParser#boolean_primary.
    def enterBoolean_primary(self, ctx:SimpAlgParser.Boolean_primaryContext):
        pass

    # Exit a parse tree produced by SimpAlgParser#boolean_primary.
    def exitBoolean_primary(self, ctx:SimpAlgParser.Boolean_primaryContext):
        pass



del SimpAlgParser