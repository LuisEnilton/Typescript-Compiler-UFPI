# Generated from TypeScript.g4 by ANTLR 4.13.2
from antlr4 import *
if "." in __name__:
    from .TypeScriptParser import TypeScriptParser
else:
    from TypeScriptParser import TypeScriptParser

# This class defines a complete listener for a parse tree produced by TypeScriptParser.
class TypeScriptListener(ParseTreeListener):

    # Enter a parse tree produced by TypeScriptParser#program.
    def enterProgram(self, ctx:TypeScriptParser.ProgramContext):
        pass

    # Exit a parse tree produced by TypeScriptParser#program.
    def exitProgram(self, ctx:TypeScriptParser.ProgramContext):
        pass


    # Enter a parse tree produced by TypeScriptParser#statement.
    def enterStatement(self, ctx:TypeScriptParser.StatementContext):
        pass

    # Exit a parse tree produced by TypeScriptParser#statement.
    def exitStatement(self, ctx:TypeScriptParser.StatementContext):
        pass


    # Enter a parse tree produced by TypeScriptParser#block.
    def enterBlock(self, ctx:TypeScriptParser.BlockContext):
        pass

    # Exit a parse tree produced by TypeScriptParser#block.
    def exitBlock(self, ctx:TypeScriptParser.BlockContext):
        pass


    # Enter a parse tree produced by TypeScriptParser#variableDecl.
    def enterVariableDecl(self, ctx:TypeScriptParser.VariableDeclContext):
        pass

    # Exit a parse tree produced by TypeScriptParser#variableDecl.
    def exitVariableDecl(self, ctx:TypeScriptParser.VariableDeclContext):
        pass


    # Enter a parse tree produced by TypeScriptParser#functionDecl.
    def enterFunctionDecl(self, ctx:TypeScriptParser.FunctionDeclContext):
        pass

    # Exit a parse tree produced by TypeScriptParser#functionDecl.
    def exitFunctionDecl(self, ctx:TypeScriptParser.FunctionDeclContext):
        pass


    # Enter a parse tree produced by TypeScriptParser#paramList.
    def enterParamList(self, ctx:TypeScriptParser.ParamListContext):
        pass

    # Exit a parse tree produced by TypeScriptParser#paramList.
    def exitParamList(self, ctx:TypeScriptParser.ParamListContext):
        pass


    # Enter a parse tree produced by TypeScriptParser#param.
    def enterParam(self, ctx:TypeScriptParser.ParamContext):
        pass

    # Exit a parse tree produced by TypeScriptParser#param.
    def exitParam(self, ctx:TypeScriptParser.ParamContext):
        pass


    # Enter a parse tree produced by TypeScriptParser#returnStmt.
    def enterReturnStmt(self, ctx:TypeScriptParser.ReturnStmtContext):
        pass

    # Exit a parse tree produced by TypeScriptParser#returnStmt.
    def exitReturnStmt(self, ctx:TypeScriptParser.ReturnStmtContext):
        pass


    # Enter a parse tree produced by TypeScriptParser#ifStmt.
    def enterIfStmt(self, ctx:TypeScriptParser.IfStmtContext):
        pass

    # Exit a parse tree produced by TypeScriptParser#ifStmt.
    def exitIfStmt(self, ctx:TypeScriptParser.IfStmtContext):
        pass


    # Enter a parse tree produced by TypeScriptParser#whileStmt.
    def enterWhileStmt(self, ctx:TypeScriptParser.WhileStmtContext):
        pass

    # Exit a parse tree produced by TypeScriptParser#whileStmt.
    def exitWhileStmt(self, ctx:TypeScriptParser.WhileStmtContext):
        pass


    # Enter a parse tree produced by TypeScriptParser#forStmt.
    def enterForStmt(self, ctx:TypeScriptParser.ForStmtContext):
        pass

    # Exit a parse tree produced by TypeScriptParser#forStmt.
    def exitForStmt(self, ctx:TypeScriptParser.ForStmtContext):
        pass


    # Enter a parse tree produced by TypeScriptParser#expressionStmt.
    def enterExpressionStmt(self, ctx:TypeScriptParser.ExpressionStmtContext):
        pass

    # Exit a parse tree produced by TypeScriptParser#expressionStmt.
    def exitExpressionStmt(self, ctx:TypeScriptParser.ExpressionStmtContext):
        pass


    # Enter a parse tree produced by TypeScriptParser#expression.
    def enterExpression(self, ctx:TypeScriptParser.ExpressionContext):
        pass

    # Exit a parse tree produced by TypeScriptParser#expression.
    def exitExpression(self, ctx:TypeScriptParser.ExpressionContext):
        pass


    # Enter a parse tree produced by TypeScriptParser#assignmentExpr.
    def enterAssignmentExpr(self, ctx:TypeScriptParser.AssignmentExprContext):
        pass

    # Exit a parse tree produced by TypeScriptParser#assignmentExpr.
    def exitAssignmentExpr(self, ctx:TypeScriptParser.AssignmentExprContext):
        pass


    # Enter a parse tree produced by TypeScriptParser#logicalOrExpr.
    def enterLogicalOrExpr(self, ctx:TypeScriptParser.LogicalOrExprContext):
        pass

    # Exit a parse tree produced by TypeScriptParser#logicalOrExpr.
    def exitLogicalOrExpr(self, ctx:TypeScriptParser.LogicalOrExprContext):
        pass


    # Enter a parse tree produced by TypeScriptParser#logicalAndExpr.
    def enterLogicalAndExpr(self, ctx:TypeScriptParser.LogicalAndExprContext):
        pass

    # Exit a parse tree produced by TypeScriptParser#logicalAndExpr.
    def exitLogicalAndExpr(self, ctx:TypeScriptParser.LogicalAndExprContext):
        pass


    # Enter a parse tree produced by TypeScriptParser#equalityExpr.
    def enterEqualityExpr(self, ctx:TypeScriptParser.EqualityExprContext):
        pass

    # Exit a parse tree produced by TypeScriptParser#equalityExpr.
    def exitEqualityExpr(self, ctx:TypeScriptParser.EqualityExprContext):
        pass


    # Enter a parse tree produced by TypeScriptParser#relationalExpr.
    def enterRelationalExpr(self, ctx:TypeScriptParser.RelationalExprContext):
        pass

    # Exit a parse tree produced by TypeScriptParser#relationalExpr.
    def exitRelationalExpr(self, ctx:TypeScriptParser.RelationalExprContext):
        pass


    # Enter a parse tree produced by TypeScriptParser#additiveExpr.
    def enterAdditiveExpr(self, ctx:TypeScriptParser.AdditiveExprContext):
        pass

    # Exit a parse tree produced by TypeScriptParser#additiveExpr.
    def exitAdditiveExpr(self, ctx:TypeScriptParser.AdditiveExprContext):
        pass


    # Enter a parse tree produced by TypeScriptParser#multiplicativeExpr.
    def enterMultiplicativeExpr(self, ctx:TypeScriptParser.MultiplicativeExprContext):
        pass

    # Exit a parse tree produced by TypeScriptParser#multiplicativeExpr.
    def exitMultiplicativeExpr(self, ctx:TypeScriptParser.MultiplicativeExprContext):
        pass


    # Enter a parse tree produced by TypeScriptParser#unaryExpr.
    def enterUnaryExpr(self, ctx:TypeScriptParser.UnaryExprContext):
        pass

    # Exit a parse tree produced by TypeScriptParser#unaryExpr.
    def exitUnaryExpr(self, ctx:TypeScriptParser.UnaryExprContext):
        pass


    # Enter a parse tree produced by TypeScriptParser#primary.
    def enterPrimary(self, ctx:TypeScriptParser.PrimaryContext):
        pass

    # Exit a parse tree produced by TypeScriptParser#primary.
    def exitPrimary(self, ctx:TypeScriptParser.PrimaryContext):
        pass


    # Enter a parse tree produced by TypeScriptParser#callExpr.
    def enterCallExpr(self, ctx:TypeScriptParser.CallExprContext):
        pass

    # Exit a parse tree produced by TypeScriptParser#callExpr.
    def exitCallExpr(self, ctx:TypeScriptParser.CallExprContext):
        pass


    # Enter a parse tree produced by TypeScriptParser#arrayAccess.
    def enterArrayAccess(self, ctx:TypeScriptParser.ArrayAccessContext):
        pass

    # Exit a parse tree produced by TypeScriptParser#arrayAccess.
    def exitArrayAccess(self, ctx:TypeScriptParser.ArrayAccessContext):
        pass


    # Enter a parse tree produced by TypeScriptParser#arrayLiteral.
    def enterArrayLiteral(self, ctx:TypeScriptParser.ArrayLiteralContext):
        pass

    # Exit a parse tree produced by TypeScriptParser#arrayLiteral.
    def exitArrayLiteral(self, ctx:TypeScriptParser.ArrayLiteralContext):
        pass


    # Enter a parse tree produced by TypeScriptParser#objectLiteral.
    def enterObjectLiteral(self, ctx:TypeScriptParser.ObjectLiteralContext):
        pass

    # Exit a parse tree produced by TypeScriptParser#objectLiteral.
    def exitObjectLiteral(self, ctx:TypeScriptParser.ObjectLiteralContext):
        pass


    # Enter a parse tree produced by TypeScriptParser#propAssign.
    def enterPropAssign(self, ctx:TypeScriptParser.PropAssignContext):
        pass

    # Exit a parse tree produced by TypeScriptParser#propAssign.
    def exitPropAssign(self, ctx:TypeScriptParser.PropAssignContext):
        pass


    # Enter a parse tree produced by TypeScriptParser#typeExpr.
    def enterTypeExpr(self, ctx:TypeScriptParser.TypeExprContext):
        pass

    # Exit a parse tree produced by TypeScriptParser#typeExpr.
    def exitTypeExpr(self, ctx:TypeScriptParser.TypeExprContext):
        pass


    # Enter a parse tree produced by TypeScriptParser#baseType.
    def enterBaseType(self, ctx:TypeScriptParser.BaseTypeContext):
        pass

    # Exit a parse tree produced by TypeScriptParser#baseType.
    def exitBaseType(self, ctx:TypeScriptParser.BaseTypeContext):
        pass


    # Enter a parse tree produced by TypeScriptParser#interfaceDecl.
    def enterInterfaceDecl(self, ctx:TypeScriptParser.InterfaceDeclContext):
        pass

    # Exit a parse tree produced by TypeScriptParser#interfaceDecl.
    def exitInterfaceDecl(self, ctx:TypeScriptParser.InterfaceDeclContext):
        pass


    # Enter a parse tree produced by TypeScriptParser#interfaceProp.
    def enterInterfaceProp(self, ctx:TypeScriptParser.InterfacePropContext):
        pass

    # Exit a parse tree produced by TypeScriptParser#interfaceProp.
    def exitInterfaceProp(self, ctx:TypeScriptParser.InterfacePropContext):
        pass


    # Enter a parse tree produced by TypeScriptParser#literal.
    def enterLiteral(self, ctx:TypeScriptParser.LiteralContext):
        pass

    # Exit a parse tree produced by TypeScriptParser#literal.
    def exitLiteral(self, ctx:TypeScriptParser.LiteralContext):
        pass



del TypeScriptParser