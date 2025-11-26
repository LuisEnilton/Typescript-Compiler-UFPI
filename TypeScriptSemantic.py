# semantic_analyzer.py
# Requer: arquivos gerados pelo ANTLR (TypeScriptLikeLexer.py, TypeScriptLikeParser.py, TypeScriptLikeVisitor.py)
# Para gerar: antlr4 -Dlanguage=Python3 TypeScriptLike.g4

from antlr4 import ParseTreeVisitor, ParserRuleContext, Token
from typing import Dict, List, Set, Optional, Any

# IMPORTS gerados pelo ANTLR - ajuste se seu gerador usar nomes diferentes
# from TypeScriptLikeParser import TypeScriptLikeParser
# from TypeScriptLikeVisitor import TypeScriptLikeVisitor

# (comentário) se o ANTLR gerou TypeScriptLikeVisitor com outro nome, ajuste os imports acima.
# Aqui vamos usar ParseTreeVisitor como fallback para manter o exemplo claro.
# Quando você rodar, substitua ParseTreeVisitor pelo visitor gerado (TypeScriptLikeVisitor).

# ----------------------------
# REPRESENTAÇÃO SIMPLES DE TIPOS
# ----------------------------
class Type:
    def name(self) -> str:
        raise NotImplementedError()
    def __str__(self):
        return self.name()

class PrimitiveType(Type):
    def __init__(self, n: str):
        self.n = n
    def name(self) -> str:
        return self.n

class ArrayType(Type):
    def __init__(self, elem: Type):
        self.elem = elem
    def name(self) -> str:
        return f"{self.elem.name()}[]"

class InterfaceType(Type):
    def __init__(self, id_: str):
        self.id = id_
        self.props: Dict[str, Type] = {}  # field -> Type
    def name(self) -> str:
        return self.id

# ----------------------------
# SÍMBOLOS
# ----------------------------
class VarSymbol:
    def __init__(self, name: str, type_: Type, is_const: bool=False):
        self.name = name
        self.type = type_
        self.is_const = is_const

class FuncSymbol:
    def __init__(self, name: str, param_types: List[Type], return_type: Type):
        self.name = name
        self.param_types = param_types
        self.return_type = return_type

# ----------------------------
# TABELA GLOBAL (simples)
# ----------------------------
class SymbolTable:
    def __init__(self):
        self.vars: Dict[str, VarSymbol] = {}
        self.funcs: Dict[str, FuncSymbol] = {}
        self.interfaces: Dict[str, InterfaceType] = {}

# ----------------------------
# ANALISADOR SEMÂNTICO (VISITOR)
# ----------------------------
class SemanticAnalyzer(ParseTreeVisitor):
    """
    Visitor que realiza checagem semântica.
    - checa interfaces
    - permite objeto literal apenas para variáveis com tipo interface
    - arrays homogêneos
    - atribuições de tipos
    - detecção de recursão indireta (apenas auto-chamada permitida)
    """

    def __init__(self):
        super().__init__()
        self.sym = SymbolTable()
        self.errors: List[str] = []
        # grafo de chamadas: func -> set(funcs que chama)
        self.call_graph: Dict[str, Set[str]] = {}
        self.current_function: Optional[str] = None
        self.expected_return_type: Optional[Type] = None

    # -------------------
    # utilitários
    # -------------------
    def _err(self, ctx: Optional[ParserRuleContext], msg: str):
        if ctx is None:
            self.errors.append(f"ERROR: {msg}")
        else:
            token: Token = ctx.start
            self.errors.append(f"Line {token.line}:{token.column} - {msg}")

    def types_equal(self, a: Type, b: Type) -> bool:
        if a is None or b is None:
            return False
        if isinstance(a, PrimitiveType) and isinstance(b, PrimitiveType):
            return a.name() == b.name()
        if isinstance(a, ArrayType) and isinstance(b, ArrayType):
            return self.types_equal(a.elem, b.elem)
        if isinstance(a, InterfaceType) and isinstance(b, InterfaceType):
            return a.name() == b.name()
        return False

    def is_assignable(self, target: Type, source: Type, ctx: Optional[ParserRuleContext]) -> bool:
        # primitives
        if isinstance(target, PrimitiveType) and isinstance(source, PrimitiveType):
            return self.types_equal(target, source)
        # arrays
        if isinstance(target, ArrayType) and isinstance(source, ArrayType):
            return self.types_equal(target, source)
        # interface assignment from object literal or same interface
        if isinstance(target, InterfaceType):
            if isinstance(source, InterfaceType):
                # source can be object-literal anon or named interface
                # check fields if source is anon (we use name "<obj-literal>")
                # require: all target props present in source and types compatible; no extras
                tgt: InterfaceType = target
                src: InterfaceType = source
                # check presence and types
                for fname, ftype in tgt.props.items():
                    if fname not in src.props:
                        self._err(ctx, f"Campo '{fname}' ausente no object literal para interface {tgt.name()}")
                        return False
                    if not self.is_assignable(ftype, src.props[fname], ctx):
                        self._err(ctx, f"Tipo do campo '{fname}' difere (esperado {ftype.name()} mas foi {src.props[fname].name()})")
                        return False
                # check extras
                for k in src.props.keys():
                    if k not in tgt.props:
                        self._err(ctx, f"Campo extra '{k}' presente no object literal não declarado na interface {tgt.name()}")
                        return False
                return True
            else:
                # source not interface (cannot assign)
                self._err(ctx, f"Atribuição para interface '{target.name()}' requer object literal compatível ou variável do mesmo tipo")
                return False
        return False

    # -------------------
    # helpers para tipos
    # -------------------
    def type_from_ctx(self, ctx) -> Optional[Type]:
        """
        Constrói um Type a partir de typeExpr (ctx). Depende da sua gramática.
        Espera: ctx.baseType() etc. Ajuste se necessário.
        """
        if ctx is None:
            return None
        # baseType could have tokens: NUMBER_TYPE, STRING_TYPE, BOOLEAN_TYPE, or ID (interface)
        # Implementação assume parser gerou methods baseType() e getText() que refletem [] no final.
        base = None
        # tenta detectar pelas propriedades (adaptar se ANTLR gerou nomes diferentes)
        try:
            bt = ctx.baseType()
            if bt is None:
                # fallback: texto
                text = ctx.getText()
                if text.endswith("[]"):
                    # try to parse element
                    inner_text = text[:-2]
                    if inner_text == "number": base = PrimitiveType("number")
                    elif inner_text == "string": base = PrimitiveType("string")
                    elif inner_text == "boolean": base = PrimitiveType("boolean")
                    else:
                        # interface name
                        it = self.sym.interfaces.get(inner_text)
                        if it is None:
                            self._err(ctx, f"Interface/tipo '{inner_text}' não declarada")
                            base = InterfaceType(f"<unknown:{inner_text}>")
                        else:
                            base = it
                    return ArrayType(base)
                else:
                    if text == "number": return PrimitiveType("number")
                    if text == "string": return PrimitiveType("string")
                    if text == "boolean": return PrimitiveType("boolean")
                    it = self.sym.interfaces.get(text)
                    if it is None:
                        self._err(ctx, f"Interface/tipo '{text}' não declarada")
                        return InterfaceType(f"<unknown:{text}>")
                    return it
            # bt exists
            if hasattr(bt, 'NUMBER_TYPE') and bt.NUMBER_TYPE() is not None:
                base = PrimitiveType("number")
            elif hasattr(bt, 'STRING_TYPE') and bt.STRING_TYPE() is not None:
                base = PrimitiveType("string")
            elif hasattr(bt, 'BOOLEAN_TYPE') and bt.BOOLEAN_TYPE() is not None:
                base = PrimitiveType("boolean")
            else:
                # ID case
                id_name = bt.ID().getText()
                it = self.sym.interfaces.get(id_name)
                if it is None:
                    self._err(ctx, f"Interface/tipo '{id_name}' não declarada")
                    base = InterfaceType(f"<unknown:{id_name}>")
                else:
                    base = it
            # array?
            if ctx.getText().endswith("[]"):
                return ArrayType(base)
            return base
        except Exception:
            # fallback: try parse by text
            txt = ctx.getText()
            if txt.endswith("[]"):
                inner = txt[:-2]
                if inner == "number": return ArrayType(PrimitiveType("number"))
                if inner == "string": return ArrayType(PrimitiveType("string"))
                if inner == "boolean": return ArrayType(PrimitiveType("boolean"))
                it = self.sym.interfaces.get(inner)
                if it is None:
                    self._err(ctx, f"Interface/tipo '{inner}' não declarada")
                    return ArrayType(InterfaceType(f"<unknown:{inner}>"))
                return ArrayType(it)
            else:
                if txt == "number": return PrimitiveType("number")
                if txt == "string": return PrimitiveType("string")
                if txt == "boolean": return PrimitiveType("boolean")
                it = self.sym.interfaces.get(txt)
                if it is None:
                    self._err(ctx, f"Interface/tipo '{txt}' não declarada")
                    return InterfaceType(f"<unknown:{txt}>")
                return it

    # -------------------
    # VISITORS (principais nós)
    # -------------------
    def visitInterfaceDecl(self, ctx):
        """ ctx: interfaceDecl """
        name = ctx.ID().getText()
        if name in self.sym.interfaces:
            self._err(ctx, f"Interface '{name}' já declarada")
            return None
        it = InterfaceType(name)
        # coleta campos
        for p in ctx.interfaceProp():
            fname = p.ID().getText()
            ftype = self.type_from_ctx(p.typeExpr())
            it.props[fname] = ftype
        self.sym.interfaces[name] = it
        return it

    def visitVariableDecl(self, ctx):
        """ ctx: variableDecl """
        # grammar: (LET|CONST) ID ':' typeExpr (ASSIGN expression)? ';'
        is_const = (ctx.LET() is None and ctx.CONST() is not None)
        name = ctx.ID().getText()
        declared = self.type_from_ctx(ctx.typeExpr())
        if name in self.sym.vars:
            self._err(ctx, f"Variável '{name}' já declarada")
            # ainda registra para evitar NPE
        self.sym.vars[name] = VarSymbol(name, declared, is_const)
        # initializer
        if ctx.ASSIGN() is not None:
            init_type = self.visit(ctx.expression())
            if not self.is_assignable(declared, init_type, ctx):
                self._err(ctx, f"Tipo de inicializador incompatível. Esperado {declared.name()} mas foi {init_type.name() if init_type else 'null'}")
        return declared

    def visitFunctionDecl(self, ctx):
        """ ctx: functionDecl """
        name = ctx.ID().getText()
        param_types = []
        if ctx.paramList() is not None:
            for p in ctx.paramList().param():
                param_types.append(self.type_from_ctx(p.typeExpr()))
        return_type = self.type_from_ctx(ctx.typeExpr())
        if name in self.sym.funcs:
            self._err(ctx, f"Função '{name}' já declarada")
        self.sym.funcs[name] = FuncSymbol(name, param_types, return_type)
        self.call_graph.setdefault(name, set())
        # analisar corpo: marcar current_function
        prev = self.current_function
        prev_expected_return = self.expected_return_type if hasattr(self, 'expected_return_type') else None
        self.current_function = name
        self.expected_return_type = return_type
        self.visit(ctx.block())
        self.current_function = prev
        self.expected_return_type = prev_expected_return
        return return_type

    def visitReturnStmt(self, ctx):
        """ ctx: returnStmt """
        # se tem expression, verifica tipo
        if ctx.expression() is not None:
            expr_type = self.visit(ctx.expression())
            if hasattr(self, 'expected_return_type') and self.expected_return_type is not None:
                if not self.is_assignable(self.expected_return_type, expr_type, ctx):
                    self._err(ctx, f"Tipo de retorno incompatível. Esperado {self.expected_return_type.name()} mas foi retornado {expr_type.name() if expr_type else 'null'}")
            return expr_type
        else:
            # return sem expressão => tipo void
            return PrimitiveType("void")

    def visitCallExpr(self, ctx):
        """ ctx: callExpr """
        called = ctx.ID().getText()
        # nativas
        if called == "read":
            if len(ctx.expression()) != 1:
                self._err(ctx, "read espera 1 argumento")
            return PrimitiveType("void")
        if called == "print":
            return PrimitiveType("void")
        # user function
        if called not in self.sym.funcs:
            self._err(ctx, f"Função '{called}' não declarada")
            return PrimitiveType("<unknown-func>")
        if self.current_function is not None:
            self.call_graph.setdefault(self.current_function, set()).add(called)
        else:
            self._err(ctx, f"Chamada a função '{called}' fora de uma função só é permitida para nativas (read/print)")
        return self.sym.funcs[called].return_type

    def visitArrayLiteral(self, ctx):
        """ ctx: arrayLiteral """
        exprs = list(ctx.expression())
        if not exprs:
            return ArrayType(PrimitiveType("unknown"))
        first = self.visit(exprs[0])
        for e in exprs[1:]:
            t = self.visit(e)
            if not self.types_equal(first, t):
                self._err(ctx, f"Array literal heterogêneo: elementos têm tipos diferentes ({first.name()} vs {t.name() if t else 'null'})")
        return ArrayType(first)

    def visitObjectLiteral(self, ctx):
        """ ctx: objectLiteral -> representamos como InterfaceType anon """
        anon = InterfaceType("<obj-literal>")
        for p in ctx.propAssign():
            key = p.ID().getText()
            val_t = self.visit(p.expression())
            anon.props[key] = val_t
        return anon

    def visitArrayAccess(self, ctx):
        """ ctx: arrayAccess """
        id_ = ctx.ID().getText()
        if id_ not in self.sym.vars:
            self._err(ctx, f"Array '{id_}' não declarado")
            return None
        vs = self.sym.vars[id_]
        if not isinstance(vs.type, ArrayType):
            self._err(ctx, f"Variável '{id_}' não é um array")
            return vs.type
        idx_type = self.visit(ctx.expression())
        if not (isinstance(idx_type, PrimitiveType) and idx_type.name() == "number"):
            self._err(ctx, "Índice de array deve ser number")
        return vs.type.elem

    def visitObjectAccess(self, ctx):
        """ ctx: objectAccess (ID '.' ID) """
        id_ = ctx.ID(0).getText()
        field = ctx.ID(1).getText()
        if id_ not in self.sym.vars:
            self._err(ctx, f"Variável '{id_}' não declarada")
            return None
        vs = self.sym.vars[id_]
        if not isinstance(vs.type, InterfaceType):
            self._err(ctx, f"Variável '{id_}' não é uma interface e não tem campos")
            return None
        if field not in vs.type.props:
            self._err(ctx, f"Campo '{field}' não existe em '{vs.type.name()}'")
            return None
        return vs.type.props[field]

    def visitLiteral(self, ctx):
        if ctx.NUMBER_LIT() is not None:
            return PrimitiveType("number")
        if ctx.STRING() is not None:
            return PrimitiveType("string")
        if ctx.BOOLEAN_LIT() is not None:
            return PrimitiveType("boolean")
        return None

    # assignmentExpr might be visited as generic node name; adapt to your generated visitor method name
    def visitAssignmentExpr(self, ctx):
        """
        ctx: assignmentExpr
        Cases:
         - ID '=' assignmentExpr
         - logicalOrExpr
        """
        # detect assign form
        text = ctx.getText()
        if '=' in text and ctx.getChildCount() >= 3:
            left = ctx.getChild(0)
            # left can be ID or arrayAccess or objectAccess; try to compute left type
            left_type = None
            if left.getPayload().__class__.__name__ == 'TerminalNodeImpl':
                # ID
                idname = left.getText()
                if idname not in self.sym.vars:
                    self._err(ctx, f"Variável '{idname}' não declarada")
                else:
                    left_type = self.sym.vars[idname].type
            else:
                # other node -> visit
                left_type = self.visit(left)
            right_type = self.visit(ctx.assignmentExpr())
            if left_type and right_type:
                if not self.is_assignable(left_type, right_type, ctx):
                    self._err(ctx, f"Atribuição de tipos incompatíveis: não é possível atribuir {right_type.name()} a {left_type.name()}")
            return left_type
        else:
            # fallback: visit children and return last type
            return self.visitChildren(ctx)

    # fallback generic visitChildren: visita filhos e retorna último tipo conhecido
    def visitChildren(self, node):
        last = None
        for i in range(node.getChildCount()):
            c = node.getChild(i)
            if hasattr(c, 'accept'):
                t = c.accept(self)
                if t is not None:
                    last = t
        return last

    # -------------------
    # pós-análise: detectar recursão indireta
    # -------------------
    def detect_indirect_recursion(self):
        visited: Set[str] = set()
        stack: Set[str] = set()

        def dfs(u: str, path: List[str]):
            visited.add(u)
            stack.add(u)
            path.append(u)
            for v in self.call_graph.get(u, set()):
                if v not in visited:
                    dfs(v, path)
                elif v in stack:
                    # achou ciclo
                    idx = path.index(v)
                    cycle = path[idx:] + [v]
                    # se ciclo contém mais de 1 função -> recursão indireta
                    nodes = list(dict.fromkeys(cycle))  # unique in order
                    if len(nodes) > 1:
                        self._err(None, f"Recursão indireta detectada: ciclo de chamadas {nodes}. Apenas recursão direta (autochamada) é permitida.")
            stack.remove(u)
            path.pop()

        for f in list(self.call_graph.keys()):
            if f not in visited:
                dfs(f, [])

    # -------------------
    # entry point
    # -------------------
    def analyze(self, tree) -> List[str]:
        # percorre a árvore
        tree.accept(self)
        # detecta recursão indireta
        self.detect_indirect_recursion()
        return self.errors

# End of semantic_analyzer.py
