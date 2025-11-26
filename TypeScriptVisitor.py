# Generated from TypeScript.g4 by ANTLR 4.13.2
from antlr4 import *
if "." in __name__:
    from .TypeScriptParser import TypeScriptParser
else:
    from TypeScriptParser import TypeScriptParser

# This class defines a complete generic visitor for a parse tree produced by TypeScriptParser.

class TypeScriptVisitor(ParseTreeVisitor):

    # Visit a parse tree produced by TypeScriptParser#program.
    def visitProgram(self, ctx:TypeScriptParser.ProgramContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TypeScriptParser#statement.
    def visitStatement(self, ctx:TypeScriptParser.StatementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TypeScriptParser#block.
    def visitBlock(self, ctx:TypeScriptParser.BlockContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TypeScriptParser#variableDecl.
    def visitVariableDecl(self, ctx:TypeScriptParser.VariableDeclContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TypeScriptParser#functionDecl.
    def visitFunctionDecl(self, ctx:TypeScriptParser.FunctionDeclContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TypeScriptParser#paramList.
    def visitParamList(self, ctx:TypeScriptParser.ParamListContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TypeScriptParser#param.
    def visitParam(self, ctx:TypeScriptParser.ParamContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TypeScriptParser#returnStmt.
    def visitReturnStmt(self, ctx:TypeScriptParser.ReturnStmtContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TypeScriptParser#ifStmt.
    def visitIfStmt(self, ctx:TypeScriptParser.IfStmtContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TypeScriptParser#whileStmt.
    def visitWhileStmt(self, ctx:TypeScriptParser.WhileStmtContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TypeScriptParser#forStmt.
    def visitForStmt(self, ctx:TypeScriptParser.ForStmtContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TypeScriptParser#expressionStmt.
    def visitExpressionStmt(self, ctx:TypeScriptParser.ExpressionStmtContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TypeScriptParser#expression.
    def visitExpression(self, ctx:TypeScriptParser.ExpressionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TypeScriptParser#assignmentExpr.
    def visitAssignmentExpr(self, ctx:TypeScriptParser.AssignmentExprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TypeScriptParser#logicalOrExpr.
    def visitLogicalOrExpr(self, ctx:TypeScriptParser.LogicalOrExprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TypeScriptParser#logicalAndExpr.
    def visitLogicalAndExpr(self, ctx:TypeScriptParser.LogicalAndExprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TypeScriptParser#equalityExpr.
    def visitEqualityExpr(self, ctx:TypeScriptParser.EqualityExprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TypeScriptParser#relationalExpr.
    def visitRelationalExpr(self, ctx:TypeScriptParser.RelationalExprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TypeScriptParser#additiveExpr.
    def visitAdditiveExpr(self, ctx:TypeScriptParser.AdditiveExprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TypeScriptParser#multiplicativeExpr.
    def visitMultiplicativeExpr(self, ctx:TypeScriptParser.MultiplicativeExprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TypeScriptParser#unaryExpr.
    def visitUnaryExpr(self, ctx:TypeScriptParser.UnaryExprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TypeScriptParser#primary.
    def visitPrimary(self, ctx:TypeScriptParser.PrimaryContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TypeScriptParser#callExpr.
    def visitCallExpr(self, ctx:TypeScriptParser.CallExprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TypeScriptParser#arrayAccess.
    def visitArrayAccess(self, ctx:TypeScriptParser.ArrayAccessContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TypeScriptParser#arrayLiteral.
    def visitArrayLiteral(self, ctx:TypeScriptParser.ArrayLiteralContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TypeScriptParser#objectLiteral.
    def visitObjectLiteral(self, ctx:TypeScriptParser.ObjectLiteralContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TypeScriptParser#propAssign.
    def visitPropAssign(self, ctx:TypeScriptParser.PropAssignContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TypeScriptParser#typeExpr.
    def visitTypeExpr(self, ctx:TypeScriptParser.TypeExprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TypeScriptParser#baseType.
    def visitBaseType(self, ctx:TypeScriptParser.BaseTypeContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TypeScriptParser#interfaceDecl.
    def visitInterfaceDecl(self, ctx:TypeScriptParser.InterfaceDeclContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TypeScriptParser#interfaceProp.
    def visitInterfaceProp(self, ctx:TypeScriptParser.InterfacePropContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TypeScriptParser#literal.
    def visitLiteral(self, ctx:TypeScriptParser.LiteralContext):
        return self.visitChildren(ctx)



del TypeScriptParser