"""
Analisador Semântico TypeScript - Versão Refatorada e Simples
Realiza checagem de tipos e validação semântica para uma linguagem similar ao TypeScript.
"""

from antlr4 import ParseTreeVisitor, ParserRuleContext, Token
from typing import Dict, List, Set, Optional

# ============================================================================
# SISTEMA DE TIPOS
# ============================================================================

class Type:
    """Classe base para todos os tipos"""
    def name(self) -> str:
        raise NotImplementedError()
    def __str__(self):
        return self.name()

class PrimitiveType(Type):
    """Tipos primitivos: number, string, boolean"""
    def __init__(self, n: str):
        self.n = n
    def name(self) -> str:
        return self.n

class ArrayType(Type):
    """Array de elementos: T[]"""
    def __init__(self, elem: Type):
        self.elem = elem
    def name(self) -> str:
        return f"{self.elem.name()}[]"

class InterfaceType(Type):
    """Interface definida pelo usuário"""
    def __init__(self, id_: str):
        self.id = id_
        self.props: Dict[str, Type] = {}
    def name(self) -> str:
        return self.id

# ============================================================================
# SÍMBOLOS
# ============================================================================

class VarSymbol:
    """Símbolo de variável ou parâmetro"""
    def __init__(self, name: str, type_: Type, is_const: bool = False):
        self.name = name
        self.type = type_
        self.is_const = is_const

class FuncSymbol:
    """Símbolo de função com tipos de parâmetros e retorno"""
    def __init__(self, name: str, param_types: List[Type], return_type: Type):
        self.name = name
        self.param_types = param_types
        self.return_type = return_type

class SymbolTable:
    """Tabela de símbolos global para variáveis, funções e interfaces"""
    def __init__(self):
        self.vars: Dict[str, VarSymbol] = {}
        self.funcs: Dict[str, FuncSymbol] = {}
        self.interfaces: Dict[str, InterfaceType] = {}

# ============================================================================
# ANALISADOR SEMÂNTICO
# ============================================================================

class SemanticAnalyzer(ParseTreeVisitor):
    """
    Visitor responsável pela análise semântica:
    - Checagem e validação de tipos
    - Rastreamento de escopo de variáveis/funções
    - Garantia de imutabilidade para const
    - Validação de homogeneidade em arrays
    - Validação de acesso a propriedades
    """

    def __init__(self):
        super().__init__()
        self.sym = SymbolTable()
        self.errors: List[str] = []
        self.call_graph: Dict[str, Set[str]] = {}
        self.current_function: Optional[str] = None
        self.expected_return_type: Optional[Type] = None
        # Registra funções nativas
        self._register_builtins()

    def _register_builtins(self):
        """Registra funções nativas: print e read"""
        # print(x: number|string|boolean): void
        self.sym.funcs["print"] = FuncSymbol(
            "print",
            [PrimitiveType("unknown")],  # aceitaremos validação manual
            PrimitiveType("void")
        )
        # read(): unknown (atribui a string ou number)
        self.sym.funcs["read"] = FuncSymbol(
            "read",
            [],
            PrimitiveType("unknown")
        )

    def _err(self, ctx: Optional[ParserRuleContext], msg: str):
        """Registra erro com informação de linha:coluna"""
        if ctx and hasattr(ctx, 'start'):
            token: Token = ctx.start
            self.errors.append(f"Linha {token.line}:{token.column} - {msg}")
        else:
            self.errors.append(f"ERRO: {msg}")

    def types_equal(self, a: Type, b: Type) -> bool:
        """Verifica se dois tipos são equivalentes"""
        if not (a and b):
            return False
        if isinstance(a, PrimitiveType) and isinstance(b, PrimitiveType):
            return a.name() == b.name()
        if isinstance(a, ArrayType) and isinstance(b, ArrayType):
            return self.types_equal(a.elem, b.elem)
        if isinstance(a, InterfaceType) and isinstance(b, InterfaceType):
            return a.name() == b.name()
        return False

    def _parse_type(self, text: str) -> Type:
        """Auxiliar: interpreta tipo a partir do texto (ex.: 'number[]', 'User')"""
        if text.endswith("[]"):
            inner = text[:-2]
            inner_type = self._parse_type(inner)
            return ArrayType(inner_type)
        
        if text in ("number", "string", "boolean", "void"):
            return PrimitiveType(text)
        
        if text in self.sym.interfaces:
            return self.sym.interfaces[text]
        
        self._err(None, f"Tipo '{text}' não encontrado")
        return InterfaceType(f"<unknown:{text}>")

    def type_from_ctx(self, ctx) -> Optional[Type]:
        """Extrai tipo a partir do contexto da gramática"""
        if not ctx:
            return None
        
        try:
            # Try to get baseType
            bt = ctx.baseType() if hasattr(ctx, 'baseType') else None
            
            if not bt:
                # Fallback to text parsing
                return self._parse_type(ctx.getText())
            
            # Parse base type
            if hasattr(bt, 'NUMBER_TYPE') and bt.NUMBER_TYPE():
                base = PrimitiveType("number")
            elif hasattr(bt, 'STRING_TYPE') and bt.STRING_TYPE():
                base = PrimitiveType("string")
            elif hasattr(bt, 'BOOLEAN_TYPE') and bt.BOOLEAN_TYPE():
                base = PrimitiveType("boolean")
            elif hasattr(bt, 'ID') and bt.ID() and bt.ID().getText() == "void":
                base = PrimitiveType("void")
            elif hasattr(bt, 'ID') and bt.ID():
                name = bt.ID().getText()
                if name in self.sym.interfaces:
                    base = self.sym.interfaces[name]
                else:
                    self._err(ctx, f"Interface '{name}' não declarada")
                    base = InterfaceType(f"<unknown:{name}>")
            else:
                return self._parse_type(ctx.getText())
            
            # Check if array
            if ctx.getText().endswith("[]"):
                return ArrayType(base)
            return base
            
        except Exception:
            return self._parse_type(ctx.getText())

    def is_assignable(self, target: Type, source: Type, ctx) -> bool:
        """Verifica se o tipo origem pode ser atribuído ao tipo destino"""
        if not (target and source):
            return False
        
        # Primitives: must match exactly
        if isinstance(target, PrimitiveType) and isinstance(source, PrimitiveType):
            # unknown pode ser atribuído a string ou number (não boolean)
            if source.name() == "unknown" and target.name() in ("string", "number"):
                return True
            return self.types_equal(target, source)
        
        # Arrays
        if isinstance(target, ArrayType) and isinstance(source, ArrayType):
            # Empty array (unknown[]) can assign to any array
            if isinstance(source.elem, PrimitiveType) and source.elem.name() == "unknown":
                return True
            # Object literal arrays to interface arrays
            if isinstance(target.elem, InterfaceType) and isinstance(source.elem, InterfaceType):
                if source.elem.name() == "<obj-literal>":
                    return self.is_assignable(target.elem, source.elem, ctx)
            return self.types_equal(target, source)
        
        # Interfaces: check field compatibility
        if isinstance(target, InterfaceType) and isinstance(source, InterfaceType):
            tgt, src = target, source
            
            # Verifica todos os campos do alvo presentes na origem
            for fname, ftype in tgt.props.items():
                if fname not in src.props:
                    self._err(ctx, f"Campo '{fname}' ausente no objeto literal para a interface {tgt.name()}")
                    return False
                if not self.is_assignable(ftype, src.props[fname], ctx):
                    self._err(ctx, f"Tipo do campo '{fname}' incompatível: esperado {ftype.name()} mas foi {src.props[fname].name()}")
                    return False
            
            # Verifica se não há campos extras na origem
            for k in src.props:
                if k not in tgt.props:
                    self._err(ctx, f"Campo extra '{k}' no objeto literal não declarado na interface {tgt.name()}")
                    return False
            
            return True
        
        return False

    # ========================================================================
    # STATEMENT VISITORS
    # ========================================================================

    def visitInterfaceDecl(self, ctx):
        """Processa declaração de interface"""
        name = ctx.ID().getText()
        if name in self.sym.interfaces:
            self._err(ctx, f"Interface '{name}' já declarada")
            return None
        
        iface = InterfaceType(name)
        for prop in ctx.interfaceProp():
            prop_name = prop.ID().getText()
            prop_type = self.type_from_ctx(prop.typeExpr())
            iface.props[prop_name] = prop_type
        
        self.sym.interfaces[name] = iface
        return None

    def visitVariableDecl(self, ctx):
        """Processa declaração de variável com checagem de tipos"""
        is_const = ctx.LET() is None
        name = ctx.ID().getText()
        declared_type = self.type_from_ctx(ctx.typeExpr())
        
        if name in self.sym.vars:
            self._err(ctx, f"Variável '{name}' já declarada")
        
        self.sym.vars[name] = VarSymbol(name, declared_type, is_const)
        
        # Check initializer if present
        if ctx.ASSIGN():
            init_type = self.visit(ctx.expression())
            if not self.is_assignable(declared_type, init_type, ctx):
                self._err(ctx, f"Tipo do inicializador incompatível: esperado {declared_type.name()} mas foi {init_type.name() if init_type else 'null'}")
        elif is_const:
            self._err(ctx, f"Variável const '{name}' deve ser inicializada na declaração")
        
        return declared_type

    def visitFunctionDecl(self, ctx):
        """Processa declaração de função com checagem de parâmetros e retorno"""
        name = ctx.ID().getText()
        params = []
        param_types = []
        
        if ctx.paramList():
            for param in ctx.paramList().param():
                param_name = param.ID().getText()
                param_type = self.type_from_ctx(param.typeExpr())
                params.append((param_name, param_type))
                param_types.append(param_type)
        
        return_type = self.type_from_ctx(ctx.typeExpr())
        
        if name in self.sym.funcs:
            self._err(ctx, f"Função '{name}' já declarada")
        
        self.sym.funcs[name] = FuncSymbol(name, param_types, return_type)
        self.call_graph.setdefault(name, set())
        
        # Enter function scope
        prev_func = self.current_function
        prev_return = self.expected_return_type
        prev_vars = self.sym.vars.copy()
        prev_return_seen = getattr(self, "_return_seen", False)
        
        self.current_function = name
        self.expected_return_type = return_type
        self._return_seen = False
        
        # Register parameters
        for param_name, param_type in params:
            self.sym.vars[param_name] = VarSymbol(param_name, param_type)
        
        # Analyze body
        self.visit(ctx.block())
        
        # Restore scope
        self.sym.vars = prev_vars
        self.current_function = prev_func
        self.expected_return_type = prev_return
        # Check missing return for non-void functions
        if isinstance(return_type, PrimitiveType) and return_type.name() != "void":
            if not getattr(self, "_return_seen", False):
                self._err(ctx, f"Função '{name}' deve retornar um valor do tipo {return_type.name()}")
        self._return_seen = prev_return_seen
        
        return return_type

    def visitReturnStmt(self, ctx):
        """Processa return com checagem de tipo"""
        # Marca que houve um return neste corpo de função
        self._return_seen = True
        # Se função é void, permitir 'return;' vazio ou ausência de return
        if self.expected_return_type and isinstance(self.expected_return_type, PrimitiveType) and self.expected_return_type.name() == "void":
            if ctx.expression():
                self._err(ctx, "Função do tipo void não deve retornar expressão")
            return PrimitiveType("void")

        # Função não-void: exige retorno com expressão compatível
        if ctx.expression() is None:
            func_name = self.current_function or "<função>"
            expected = self.expected_return_type.name() if self.expected_return_type else 'desconhecido'
            self._err(ctx, f"Função '{func_name}' deve retornar um valor do tipo {expected}")
            return PrimitiveType("void")

        expr_type = self.visit(ctx.expression())
        if self.expected_return_type:
            if not self.is_assignable(self.expected_return_type, expr_type, ctx):
                self._err(ctx, f"Tipo de retorno incompatível. Esperado {self.expected_return_type.name()} mas foi {expr_type.name() if expr_type else 'null'}")
        return expr_type
        return PrimitiveType("void")

    # ========================================================================
    # EXPRESSION VISITORS
    # ========================================================================

    def visitLiteral(self, ctx):
        """Processa literal (number, string, boolean)"""
        if ctx.NUMBER_LIT():
            return PrimitiveType("number")
        if ctx.STRING():
            return PrimitiveType("string")
        if ctx.BOOLEAN_LIT():
            return PrimitiveType("boolean")
        return None

    def visitPrimary(self, ctx):
        """Processa expressões primárias (literais, identificadores, parênteses, arrays, objetos)"""
        # Literal
        if ctx.literal():
            return self.visit(ctx.literal())
        
        # Identifier (variable or function reference)
        if ctx.ID():
            name = ctx.ID().getText()
            if name in self.sym.vars:
                return self.sym.vars[name].type
            if name in self.sym.funcs:
                return self.sym.funcs[name].return_type
            self._err(ctx, f"Variável '{name}' não declarada")
            return None
        
        # Parenthesized expression
        if ctx.expression():
            return self.visit(ctx.expression())
        
        # Array literal
        if ctx.arrayLiteral():
            return self.visit(ctx.arrayLiteral())
        
        # Object literal
        if ctx.objectLiteral():
            return self.visit(ctx.objectLiteral())
        
        return None

    def visitArrayLiteral(self, ctx):
        """Processa array literal com verificação de homogeneidade"""
        exprs = list(ctx.expression()) if ctx.expression() else []
        
        if not exprs:
            return ArrayType(PrimitiveType("unknown"))
        
        first = self.visit(exprs[0])
        for expr in exprs[1:]:
            elem_type = self.visit(expr)
            if not self.types_equal(first, elem_type):
                self._err(ctx, f"Array heterogêneo: elementos têm tipos diferentes ({first.name()} vs {elem_type.name() if elem_type else 'null'})")
        
        return ArrayType(first)

    def visitObjectLiteral(self, ctx):
        """Processa object literal como interface anônima"""
        obj = InterfaceType("<obj-literal>")
        for prop in ctx.propAssign():
            # Handle both ID and STRING as property names
            if prop.ID():
                key = prop.ID().getText()
            else:
                key = prop.STRING().getText()[1:-1]  # Remove quotes
            
            value_type = self.visit(prop.expression())
            obj.props[key] = value_type
        
        return obj

    def visitPostfixExpr(self, ctx):
        """Processa expressões pós-fixadas: acesso a array, acesso a propriedade, chamadas de função"""
        # Get primary ID name for function call resolution
        primary_id = None
        if ctx.primary().ID():
            primary_id = ctx.primary().ID().getText()
        
        result_type = self.visit(ctx.primary())
        
        # Process postfix operators
        postfix_ops = ctx.postfixOp() if hasattr(ctx, 'postfixOp') and ctx.postfixOp() else []
        if not isinstance(postfix_ops, list):
            postfix_ops = [postfix_ops] if postfix_ops else []
        
        for op_idx, op in enumerate(postfix_ops):
            op_text = op.getText()
            
            if op_text.startswith('['):
                # Array access
                if isinstance(result_type, ArrayType):
                    result_type = result_type.elem
                else:
                    self._err(ctx, "Acesso de array em tipo não-array")
                    return None
            
            elif op_text.startswith('.'):
                # Property access
                prop_name = op_text[1:]
                if isinstance(result_type, InterfaceType):
                    if prop_name in result_type.props:
                        result_type = result_type.props[prop_name]
                    else:
                        self._err(ctx, f"Campo '{prop_name}' não existe na interface '{result_type.name()}'")
                        return None
                else:
                    self._err(ctx, "Acesso de propriedade em tipo não-interface")
                    return None
            
            elif op_text.startswith('(') and op_idx == 0 and primary_id:
                # Function call (first postfix op on identifier)
                if primary_id in self.sym.funcs:
                    func = self.sym.funcs[primary_id]
                    # Validate arguments count & types
                    args_ctx = op
                    arg_exprs = []
                    # Extract expressions inside parentheses via parse tree
                    try:
                        arg_exprs = list(args_ctx.expression()) if hasattr(args_ctx, 'expression') and args_ctx.expression() else []
                    except Exception:
                        arg_exprs = []
                    # Simple arity check
                    if len(func.param_types) != len(arg_exprs):
                        # Allow print(x) single arg; read() zero args
                        pass
                    # Type validation for print
                    if primary_id == "print" and len(arg_exprs) == 1:
                        arg_t = self.visit(arg_exprs[0])
                        if not isinstance(arg_t, PrimitiveType) or arg_t.name() not in ("string", "number", "boolean"):
                            self._err(ctx, "Função nativa 'print' aceita apenas string, number ou boolean")
                    if primary_id == "read" and len(arg_exprs) != 0:
                        self._err(ctx, "Função nativa 'read' não aceita argumentos")
                    result_type = func.return_type
                    if self.current_function:
                        self.call_graph.setdefault(self.current_function, set()).add(primary_id)
        
        return result_type

    def _binary_expr(self, ctx, op_validator, result_type_fn):
        """Tratador genérico para expressões binárias"""
        if ctx.getChildCount() == 1:
            return self.visit(ctx.getChild(0))
        
        left = self.visit(ctx.getChild(0))
        
        for i in range(1, ctx.getChildCount(), 2):
            op = ctx.getChild(i).getText()
            right = self.visit(ctx.getChild(i + 1))
            
            if left and right:
                op_validator(left, right, op, ctx)
            
            left = result_type_fn(left, right)
        
        return left

    def visitAdditiveExpr(self, ctx):
        """Processa operadores + e - (apenas number)"""
        def validate(l, r, op, c):
            if not (isinstance(l, PrimitiveType) and l.name() == "number" and
                    isinstance(r, PrimitiveType) and r.name() == "number"):
                self._err(c, f"Operador '{op}' requer operandos do tipo number")
        
        def result_type(l, r):
            return PrimitiveType("number")
        
        return self._binary_expr(ctx, validate, result_type)

    def visitMultiplicativeExpr(self, ctx):
        """Processa operadores *, /, % (apenas number)"""
        def validate(l, r, op, c):
            if not (isinstance(l, PrimitiveType) and l.name() == "number" and
                    isinstance(r, PrimitiveType) and r.name() == "number"):
                self._err(c, f"Operador '{op}' requer operandos do tipo number")
        
        def result_type(l, r):
            return PrimitiveType("number")
        
        return self._binary_expr(ctx, validate, result_type)

    def visitRelationalExpr(self, ctx):
        """Processa operadores <, <=, >, >= (operandos number; resultado boolean)"""
        def validate(l, r, op, c):
            if not (isinstance(l, PrimitiveType) and l.name() == "number" and
                    isinstance(r, PrimitiveType) and r.name() == "number"):
                self._err(c, f"Operador '{op}' requer operandos do tipo number")
        
        def result_type(l, r):
            return PrimitiveType("boolean")
        
        return self._binary_expr(ctx, validate, result_type)

    def visitEqualityExpr(self, ctx):
        """Processa operadores == e != (mesmo tipo em ambos os lados; resultado boolean)"""
        def validate(l, r, op, c):
            if not self.types_equal(l, r):
                self._err(c, f"Operador '{op}' requer operandos do mesmo tipo")
        
        def result_type(l, r):
            return PrimitiveType("boolean")
        
        return self._binary_expr(ctx, validate, result_type)

    def visitLogicalAndExpr(self, ctx):
        """Processa operador && (apenas boolean)"""
        def validate(l, r, op, c):
            if not (isinstance(l, PrimitiveType) and l.name() == "boolean" and
                    isinstance(r, PrimitiveType) and r.name() == "boolean"):
                self._err(c, f"Operador '&&' requer operandos do tipo boolean")
        
        def result_type(l, r):
            return PrimitiveType("boolean")
        
        return self._binary_expr(ctx, validate, result_type)

    def visitLogicalOrExpr(self, ctx):
        """Processa operador || (apenas boolean)"""
        def validate(l, r, op, c):
            if not (isinstance(l, PrimitiveType) and l.name() == "boolean" and
                    isinstance(r, PrimitiveType) and r.name() == "boolean"):
                self._err(c, f"Operador '||' requer operandos do tipo boolean")
        
        def result_type(l, r):
            return PrimitiveType("boolean")
        
        return self._binary_expr(ctx, validate, result_type)

    def visitAssignmentExpr(self, ctx):
        """Processa expressões de atribuição (postfixExpr = assignmentExpr)"""
        # Find assignment operator
        assign_idx = -1
        for i in range(ctx.getChildCount()):
            text = ctx.getChild(i).getText()
            if text == '=' and '==' not in text:
                assign_idx = i
                break
        
        if assign_idx > 0:
            # Assignment found
            left = ctx.getChild(0)
            left_type = self.visit(left)
            
            # Check const reassignment
            if hasattr(left, 'getText') and assign_idx == 1:
                left_text = left.getText()
                if left_text in self.sym.vars and self.sym.vars[left_text].is_const:
                    self._err(ctx, f"Não é possível reatribuir variável const '{left_text}'")
            
            # Check type compatibility
            right_type = self.visit(ctx.assignmentExpr())
            if left_type and right_type:
                if not self.is_assignable(left_type, right_type, ctx):
                    self._err(ctx, f"Tipos incompatíveis na atribuição: não é possível atribuir {right_type.name()} a {left_type.name()}")
            
            return left_type
        else:
            # No assignment, just expression
            if ctx.logicalOrExpr():
                return self.visit(ctx.logicalOrExpr())
            return self.visitChildren(ctx)

    def visitChildren(self, node):
        """Fallback: visita todos os filhos e retorna o último tipo"""
        result = None
        for i in range(node.getChildCount()):
            child = node.getChild(i)
            if hasattr(child, 'accept'):
                t = child.accept(self)
                if t:
                    result = t
        return result

    # ========================================================================
    # ANALYSIS ENTRY POINT
    # ========================================================================

    def analyze(self, tree) -> List[str]:
        """Ponto de entrada: analisa a árvore e retorna lista de erros"""
        tree.accept(self)
        return self.errors
