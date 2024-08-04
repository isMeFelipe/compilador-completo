# Generated from SimpAlg.g4 by ANTLR 4.9.2
from antlr4 import *
if __name__ is not None and "." in __name__:
    from .SimpAlgParser import SimpAlgParser
else:
    from SimpAlgParser import SimpAlgParser

# This class defines a complete generic visitor for a parse tree produced by SimpAlgParser.

class SimpAlgVisitor(ParseTreeVisitor):

    # Visit a parse tree produced by SimpAlgParser#program.
    def visitProgram(self, ctx:SimpAlgParser.ProgramContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SimpAlgParser#statement_list.
    def visitStatement_list(self, ctx:SimpAlgParser.Statement_listContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SimpAlgParser#statement.
    def visitStatement(self, ctx:SimpAlgParser.StatementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SimpAlgParser#declaration.
    def visitDeclaration(self, ctx:SimpAlgParser.DeclarationContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SimpAlgParser#variable_list.
    def visitVariable_list(self, ctx:SimpAlgParser.Variable_listContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SimpAlgParser#t_type.
    def visitT_type(self, ctx:SimpAlgParser.T_typeContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SimpAlgParser#assignment.
    def visitAssignment(self, ctx:SimpAlgParser.AssignmentContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SimpAlgParser#io_statement.
    def visitIo_statement(self, ctx:SimpAlgParser.Io_statementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SimpAlgParser#value_list.
    def visitValue_list(self, ctx:SimpAlgParser.Value_listContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SimpAlgParser#value.
    def visitValue(self, ctx:SimpAlgParser.ValueContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SimpAlgParser#if_statement.
    def visitIf_statement(self, ctx:SimpAlgParser.If_statementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SimpAlgParser#repeat_statement.
    def visitRepeat_statement(self, ctx:SimpAlgParser.Repeat_statementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SimpAlgParser#goto_statement.
    def visitGoto_statement(self, ctx:SimpAlgParser.Goto_statementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SimpAlgParser#label_declaration.
    def visitLabel_declaration(self, ctx:SimpAlgParser.Label_declarationContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SimpAlgParser#expression.
    def visitExpression(self, ctx:SimpAlgParser.ExpressionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SimpAlgParser#term.
    def visitTerm(self, ctx:SimpAlgParser.TermContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SimpAlgParser#factor.
    def visitFactor(self, ctx:SimpAlgParser.FactorContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SimpAlgParser#primary.
    def visitPrimary(self, ctx:SimpAlgParser.PrimaryContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SimpAlgParser#boolean_expression.
    def visitBoolean_expression(self, ctx:SimpAlgParser.Boolean_expressionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SimpAlgParser#boolean_term.
    def visitBoolean_term(self, ctx:SimpAlgParser.Boolean_termContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SimpAlgParser#boolean_factor.
    def visitBoolean_factor(self, ctx:SimpAlgParser.Boolean_factorContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SimpAlgParser#boolean_primary.
    def visitBoolean_primary(self, ctx:SimpAlgParser.Boolean_primaryContext):
        return self.visitChildren(ctx)



del SimpAlgParser