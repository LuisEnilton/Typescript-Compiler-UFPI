from antlr4 import ParseTreeVisitor
from TypeScriptParser import TypeScriptParser
# Importamos as classes de tipo do seu analisador semântico para referência
from TypeScriptSemantic import PrimitiveType, ArrayType, InterfaceType


class JasminGenerator(ParseTreeVisitor):
    def __init__(self, semantic_analyzer, class_name="Output"):
        self.sem = semantic_analyzer
        self.class_name = class_name
        self.code = []  # Lista para armazenar as linhas do código Jasmin

        # Controle de Labels e Locals
        self.label_counter = 0
        self.local_var_index = 0
        self.local_vars = {}  # Mapa {nome: indice_jvm} para o escopo atual

        # Controle de Stack (simplificado: assumimos um limite seguro)
        self.stack_limit = 200
        self.locals_limit = 200

    def emit(self, instr):
        """Adiciona uma instrução à lista de código"""
        self.code.append(f"    {instr}")

    def emit_label(self, label):
        """Adiciona um label"""
        self.code.append(f"{label}:")

    def get_new_label(self):
        """Gera um label único"""
        self.label_counter += 1
        return f"L{self.label_counter}"

    def get_jvm_type(self, ts_type):
        """Converte tipos do TypeScript para descritores JVM"""
        if isinstance(ts_type, PrimitiveType):
            if ts_type.name() == "number":
                return "I"  # Int
            if ts_type.name() == "boolean":
                return "I"  # Boolean é int (0/1)
            if ts_type.name() == "string":
                return "Ljava/lang/String;"
            if ts_type.name() == "void":
                return "V"
        if isinstance(ts_type, ArrayType):
            # Usamos java.util.ArrayList como representação
            return "Ljava/util/ArrayList;"
        # Default/Fallback
        return "I"

    def get_result(self):
        """Retorna o código Jasmin completo"""
        return "\n".join(self.code)

    # ========================================================================
    # VISITORS PRINCIPAIS
    # ========================================================================

    def visitProgram(self, ctx: TypeScriptParser.ProgramContext):
        # Cabeçalho da Classe
        self.code.append(f".class public {self.class_name}")
        self.code.append(".super java/lang/Object")
        self.code.append("")

        # 1. Gerar Fields Estáticos (Variáveis Globais)
        # O analisador semântico já identificou as globais em self.sem.sym.global_vars
        for name, symbol in self.sem.sym.global_vars.items():
            desc = self.get_jvm_type(symbol.type)
            self.code.append(f".field public static {name} {desc}")

        self.code.append("")

        # 1.5. Bloco inicializador estático (<clinit>) para inicializar variáveis globais
        # Isto é importante para garantir que as variáveis estáticas sejam inicializadas
        # antes de qualquer código acessá-las - mas APENAS as com inicializadores simples
        if self.sem.sym.global_vars:
            self.code.append(".method public static <clinit>()V")
            self.emit(f".limit stack {self.stack_limit}")
            self.emit(f".limit locals {self.locals_limit}")

            # NÃO processamos aqui! O <clinit> servirá apenas como marcador
            # As variáveis globais com inicializadores dinâmicos devem ser inicializadas no main
            # Se REALMENTE necessário, você poderia adicionar suporte a inicializadores constantes aqui

            self.emit("return")
            self.code.append(".end method")
            self.code.append("")

        # 2. Construtor Padrão (Obrigatório na JVM)
        self.code.append(".method public <init>()V")
        self.emit("aload_0")
        # Em Jasmin, o construtor de super é chamado via invokespecial
        self.emit("invokespecial java/lang/Object/<init>()V")
        self.emit("return")
        self.code.append(".end method")
        self.code.append("")

        # 3. Gerar métodos/funções
        # Visitamos os filhos para gerar as funções definidas
        for child in ctx.children:
            if isinstance(child, TypeScriptParser.StatementContext):
                # Se for declaração de função, visitamos
                if child.functionDecl():
                    self.visit(child.functionDecl())

        # 4. Método Main Java (Ponto de entrada)
        # Este método encapsula o código "solto" do script e chama a função main se existir
        self.code.append(".method public static main([Ljava/lang/String;)V")
        self.emit(f".limit stack {self.stack_limit}")
        self.emit(f".limit locals {self.locals_limit}")

        # Executa statements globais (que não são funções nem declarações de tipo)
        self.local_vars = {}  # Reinicia locais para o main
        self.local_var_index = 1  # 0 é args, começamos do 1

        for child in ctx.children:
            if isinstance(child, TypeScriptParser.StatementContext):
                # Processa todos os statements globais (incluindo declarações de variáveis)
                # que precisam ser inicializadas em runtime
                if not child.functionDecl() and not child.interfaceDecl():
                    self.visit(child)

        self.emit("return")
        self.code.append(".end method")

    def visitFunctionDecl(self, ctx: TypeScriptParser.FunctionDeclContext):
        func_name = ctx.ID().getText()
        # Recupera informações da tabela de símbolos do analisador semântico
        func_symbol = self.sem.sym.funcs.get(func_name)

        if not func_symbol:
            return  # Não deve acontecer se a semântica passou

        # Monta assinatura JVM: (II)V, (Ljava/lang/String;)I, etc.
        param_desc = ""
        for p_type in func_symbol.param_types:
            param_desc += self.get_jvm_type(p_type)

        return_desc = self.get_jvm_type(func_symbol.return_type)

        self.code.append(
            f".method public static {func_name}({param_desc}){return_desc}")
        self.emit(f".limit stack {self.stack_limit}")
        self.emit(f".limit locals {self.locals_limit}")

        # Reseta mapa de variáveis locais para esta função
        self.local_vars = {}
        self.local_var_index = 0

        # Mapeia parâmetros para índices locais (0, 1, 2...)
        if ctx.paramList():
            for param in ctx.paramList().param():
                p_name = param.ID().getText()
                self.local_vars[p_name] = self.local_var_index
                self.local_var_index += 1

        # Visita o corpo da função
        self.visit(ctx.block())

        # Adiciona return void se faltar (segurança)
        if return_desc == "V":
            self.emit("return")
        # Se for int/bool e não tiver return, a JVM vai reclamar, mas o código fonte deveria ter
        # O analisador semântico garante que tem return se não for void.

        self.code.append(".end method")
        self.code.append("")

    # ========================================================================
    # STATEMENTS
    # ========================================================================

    def visitVariableDecl(self, ctx: TypeScriptParser.VariableDeclContext):
        # Delega para let/const conforme a regra
        if ctx.letDecl():
            return self.visit(ctx.letDecl())
        if ctx.constDecl():
            return self.visit(ctx.constDecl())
        return None

    def visitLetDecl(self, ctx: TypeScriptParser.LetDeclContext):
        return self._visitVarDecl_common(ctx)

    def visitConstDecl(self, ctx: TypeScriptParser.ConstDeclContext):
        return self._visitVarDecl_common(ctx)

    def _visitVarDecl_common(self, ctx):
        name = ctx.ID().getText()

        # Se tem inicialização (ex: let x = 10)
        if ctx.expression():
            # 1. Gera código da expressão (deixa valor na pilha)
            self.visit(ctx.expression())

            # 2. Armazena o valor
            if name in self.local_vars:
                # É reatribuição de variável local existente
                idx = self.local_vars[name]
                expr_text = ctx.expression().getText() if ctx.expression() else ""
                if expr_text.startswith("array("):
                    self.emit(f"astore {idx}")
                else:
                    self.emit(f"istore {idx}")
            elif name in self.sem.sym.global_vars:
                # É uma variável global (declarada no nível superior do programa)
                var_sym = self.sem.sym.global_vars[name]
                desc = self.get_jvm_type(var_sym.type)
                self.emit(f"putstatic {self.class_name}/{name} {desc}")
            else:
                # Nova variável local dentro de um método
                idx = self.local_var_index
                self.local_vars[name] = idx
                self.local_var_index += 1

                # Check type for correct store instruction
                expr_text = ctx.expression().getText() if ctx.expression() else ""
                if expr_text.startswith("array("):
                    self.emit(f"astore {idx}")
                else:
                    self.emit(f"istore {idx}")

    def visitExpressionStmt(self, ctx: TypeScriptParser.ExpressionStmtContext):
        """Visita um statement de expressão: expr;
        Se a expressão deixa um valor na pilha, é necessário descartá-lo."""
        expr_ctx = ctx.expression()

        # Verifica se é uma chamada de função que retorna void
        expr_text = expr_ctx.getText() if expr_ctx else ""

        # Funções que não deixam valor na pilha (retornam void)
        # print() e push() retornam void
        # pop() e size() retornam valor
        # Também detecta .push() como método
        is_void_func = (expr_text.startswith("print(") or
                        expr_text.startswith("push(") or
                        ".push(" in expr_text)

        self.visit(expr_ctx)

        # Se não é função void, há um valor na pilha que precisa ser descartado
        if not is_void_func:
            self.emit("pop")

    def visitIfStmt(self, ctx: TypeScriptParser.IfStmtContext):
        label_else = self.get_new_label()
        label_end = self.get_new_label()

        # Avalia expressão
        self.visit(ctx.expression())

        # Se 0 (false), pula para else
        self.emit(f"ifeq {label_else}")

        # Bloco Then
        self.visit(ctx.statement(0))
        self.emit(f"goto {label_end}")

        # Bloco Else
        self.emit_label(label_else)
        # Regra ifStmt tem else opcional com token ELSE
        if ctx.getChildCount() > 0:
            try:
                self.visit(ctx.statement(1))
            except Exception:
                pass

        self.emit_label(label_end)

    def visitWhileStmt(self, ctx: TypeScriptParser.WhileStmtContext):
        label_start = self.get_new_label()
        label_end = self.get_new_label()

        self.emit_label(label_start)

        # Condição
        self.visit(ctx.expression())
        self.emit(f"ifeq {label_end}")

        # Corpo
        self.visit(ctx.statement())
        self.emit(f"goto {label_start}")

        self.emit_label(label_end)

    def visitForStmt(self, ctx: TypeScriptParser.ForStmtContext):
        """Processa for(init; cond; update) body"""
        label_start = self.get_new_label()
        label_end = self.get_new_label()

        # 1. Inicialização (variableDecl ou expressionStmt)
        if hasattr(ctx, 'variableDecl') and ctx.variableDecl():
            self.visit(ctx.variableDecl())
        elif hasattr(ctx, 'expressionStmt') and ctx.expressionStmt():
            self.visit(ctx.expressionStmt())

        # 2. Loop start
        self.emit_label(label_start)

        # 3. Condição
        if hasattr(ctx, 'expression') and ctx.expression() and len(ctx.expression()) > 0:
            self.visit(ctx.expression(0))
            self.emit(f"ifeq {label_end}")

        # 4. Corpo
        self.visit(ctx.statement())

        # 5. Update
        if hasattr(ctx, 'expression') and ctx.expression() and len(ctx.expression()) > 1:
            self.visit(ctx.expression(1))
            # O update pode deixar um valor na pilha; descartar
            self.emit("pop")

        # 6. Voltar ao start
        self.emit(f"goto {label_start}")

        # 7. End label
        self.emit_label(label_end)

    def visitReturnStmt(self, ctx: TypeScriptParser.ReturnStmtContext):
        if ctx.expression():
            self.visit(ctx.expression())
            self.emit("ireturn")  # Assumindo int/bool
        else:
            self.emit("return")

    # ========================================================================
    # EXPRESSÕES
    # ========================================================================

    def visitAssignmentExpr(self, ctx: TypeScriptParser.AssignmentExprContext):
        # Se tem atribuição (ex: x = 10)
        if ctx.ASSIGN():
            # Lado direito (valor)
            self.visit(ctx.assignmentExpr())

            # Lado esquerdo (variável)
            # Precisamos do nome. O lado esquerdo é um ternaryExpr -> ... -> primary -> ID
            # Essa navegação na árvore crua é chata. Vamos tentar pegar o texto.
            # Nota: Isso é uma simplificação. O correto seria visitar o lado esquerdo
            # num modo "L-Value" (obter endereço) em vez de "R-Value" (obter valor).
            var_name = ctx.getChild(0).getText()

            if var_name in self.local_vars:
                idx = self.local_vars[var_name]
                # Mantém valor na pilha para encadeamento (a = b = c)
                self.emit("dup")
                self.emit(f"istore {idx}")
            elif var_name in self.sem.sym.global_vars:
                desc = self.get_jvm_type(
                    self.sem.sym.global_vars[var_name].type)
                self.emit("dup")
                self.emit(f"putstatic {self.class_name}/{var_name} {desc}")
        else:
            # Pass-through: delega para expressão lógica (topo da cadeia)
            if hasattr(ctx, 'logicalOrExpr') and ctx.logicalOrExpr():
                self.visit(ctx.logicalOrExpr())

    def visitAdditiveExpr(self, ctx: TypeScriptParser.AdditiveExprContext):
        # Efetua operações da esquerda para a direita
        self.visit(ctx.multiplicativeExpr(0))

        for i in range(1, len(ctx.multiplicativeExpr())):
            self.visit(ctx.multiplicativeExpr(i))
            op = ctx.getChild(i*2 - 1).getText()  # +, -
            if op == '+':
                self.emit("iadd")
            elif op == '-':
                self.emit("isub")

    def visitMultiplicativeExpr(self, ctx: TypeScriptParser.MultiplicativeExprContext):
        self.visit(ctx.unaryExpr(0))
        for i in range(1, len(ctx.unaryExpr())):
            self.visit(ctx.unaryExpr(i))
            op = ctx.getChild(i*2 - 1).getText()
            if op == '*':
                self.emit("imul")
            elif op == '/':
                self.emit("idiv")
            elif op == '%':
                self.emit("irem")

    def visitRelationalExpr(self, ctx: TypeScriptParser.RelationalExprContext):
        if len(ctx.additiveExpr()) == 1:
            self.visit(ctx.additiveExpr(0))
            return

        self.visit(ctx.additiveExpr(0))
        self.visit(ctx.additiveExpr(1))

        op = ctx.getChild(1).getText()
        true_label = self.get_new_label()
        end_label = self.get_new_label()

        if op == '<':
            self.emit(f"if_icmplt {true_label}")
        elif op == '>':
            self.emit(f"if_icmpgt {true_label}")
        elif op == '<=':
            self.emit(f"if_icmple {true_label}")
        elif op == '>=':
            self.emit(f"if_icmpge {true_label}")

        self.emit("iconst_0")  # False
        self.emit(f"goto {end_label}")
        self.emit_label(true_label)
        self.emit("iconst_1")  # True
        self.emit_label(end_label)

    def visitEqualityExpr(self, ctx: TypeScriptParser.EqualityExprContext):
        if len(ctx.relationalExpr()) == 1:
            self.visit(ctx.relationalExpr(0))
            return

        self.visit(ctx.relationalExpr(0))
        self.visit(ctx.relationalExpr(1))

        op = ctx.getChild(1).getText()
        true_label = self.get_new_label()
        end_label = self.get_new_label()

        if '==' in op:
            # Trata == e === igual para int
            self.emit(f"if_icmpeq {true_label}")
        if '!=' in op:
            self.emit(f"if_icmpne {true_label}")

        self.emit("iconst_0")
        self.emit(f"goto {end_label}")
        self.emit_label(true_label)
        self.emit("iconst_1")
        self.emit_label(end_label)

    def visitPrimary(self, ctx: TypeScriptParser.PrimaryContext):
        if ctx.literal():
            self.visit(ctx.literal())
        elif ctx.arrayLiteral():
            # Suporta [] - cria novo ArrayList vazio
            self.emit("new java/util/ArrayList")
            self.emit("dup")
            self.emit("invokespecial java/util/ArrayList/<init>()V")
        elif ctx.ID():
            name = ctx.ID().getText()
            if name in self.local_vars:
                idx = self.local_vars[name]
                self.emit(f"iload {idx}")
            elif name in self.sem.sym.global_vars:
                desc = self.get_jvm_type(self.sem.sym.global_vars[name].type)
                self.emit(f"getstatic {self.class_name}/{name} {desc}")
        elif ctx.expression():
            self.visit(ctx.expression())

    def visitLiteral(self, ctx: TypeScriptParser.LiteralContext):
        if ctx.NUMBER_LIT():
            val = ctx.NUMBER_LIT().getText()
            # Truncate float to int for simplicity in this implementation
            if '.' in val:
                val = str(int(float(val)))
            self.emit(f"ldc {val}")
        elif ctx.BOOLEAN_LIT():
            val = 1 if ctx.BOOLEAN_LIT().getText() == 'true' else 0
            self.emit(f"iconst_{val}")
        elif ctx.STRING():
            self.emit(f"ldc {ctx.STRING().getText()}")

    def visitPostfixExpr(self, ctx: TypeScriptParser.PostfixExprContext):
        primary = ctx.primary()

        if not ctx.postfixOp():
            self.visit(primary)
            return

        # Processa todos os postfixOp em sequência
        ops = [ctx.postfixOp(i) for i in range(ctx.getChildCount() - 1)]

        # Detecta padrão: .método seguido por (argumentos)
        # arr.push(10) → [.push, (10)]
        # arr.pop() → [.pop, ()]
        i = 0
        self.visit(primary)  # Carrega o primary inicialmente

        while i < len(ops):
            op = ops[i]
            op_text = op.getText()

            # Acesso por índice: arr[i]
            if op_text.startswith('['):
                if hasattr(op, 'expression') and op.expression():
                    self.visit(op.expression()[0])
                self.emit(
                    "invokevirtual java/util/ArrayList/get(I)Ljava/lang/Object;")
                self.emit("checkcast java/lang/Integer")
                self.emit("invokevirtual java/lang/Integer/intValue()I")
                i += 1
                continue

            # Métodos de array com possível argumento no próximo postfixOp
            if op_text.startswith('.'):
                method_name = op_text[1:]  # Remove o ponto
                next_op = ops[i + 1] if i + 1 < len(ops) else None

                if method_name == "push" and next_op and next_op.getText().startswith('('):
                    # arr.push(val)
                    # O valor está em next_op.expression()
                    arg_exprs = list(next_op.expression()) if hasattr(
                        next_op, 'expression') and next_op.expression() else []
                    if len(arg_exprs) >= 1:
                        self.visit(arg_exprs[0])
                        self.emit(
                            "invokestatic java/lang/Integer/valueOf(I)Ljava/lang/Integer;")
                        self.emit(
                            "invokevirtual java/util/ArrayList/add(Ljava/lang/Object;)Z")
                        self.emit("pop")
                    i += 2  # Consome dois postfixOp
                    continue

                if method_name == "pop" and next_op and next_op.getText().startswith('('):
                    # arr.pop()
                    temp_var = 99
                    self.emit("dup")
                    self.emit("invokevirtual java/util/ArrayList/size()I")
                    self.emit("iconst_1")
                    self.emit("isub")
                    self.emit("dup")
                    self.emit(f"istore {temp_var}")
                    self.emit(
                        "invokevirtual java/util/ArrayList/remove(I)Ljava/lang/Object;")
                    self.emit("checkcast java/lang/Integer")
                    self.emit("invokevirtual java/lang/Integer/intValue()I")
                    i += 2  # Consome dois postfixOp
                    continue

                if method_name == "size" and next_op and next_op.getText().startswith('('):
                    # arr.size()
                    self.emit("invokevirtual java/util/ArrayList/size()I")
                    i += 2  # Consome dois postfixOp
                    continue

            # Chamadas de função regular (sem ponto)
            if op_text.startswith('('):
                if primary.ID():
                    func_name = primary.ID().getText()
                    arg_exprs = list(op.expression()) if hasattr(
                        op, 'expression') and op.expression() else []

                    if func_name == "print":
                        self.emit(
                            "getstatic java/lang/System/out Ljava/io/PrintStream;")
                        if arg_exprs:
                            if len(arg_exprs) == 1:
                                self.visit(arg_exprs[0])
                                arg_text = arg_exprs[0].getText()
                                if (arg_text.startswith('"') and arg_text.endswith('"')) or (arg_text.startswith("'") and arg_text.endswith("'")):
                                    self.emit(
                                        "invokevirtual java/io/PrintStream/println(Ljava/lang/String;)V")
                                else:
                                    self.emit(
                                        "invokevirtual java/io/PrintStream/println(I)V")
                            else:
                                self.emit("new java/lang/StringBuilder")
                                self.emit("dup")
                                self.emit(
                                    "invokespecial java/lang/StringBuilder/<init>()V")

                                for idx, arg in enumerate(arg_exprs):
                                    if idx > 0:
                                        self.emit("ldc \" \"")
                                        self.emit(
                                            "invokevirtual java/lang/StringBuilder/append(Ljava/lang/String;)Ljava/lang/StringBuilder;")

                                    self.visit(arg)
                                    arg_text = arg.getText()
                                    if (arg_text.startswith('"') and arg_text.endswith('"')) or (arg_text.startswith("'") and arg_text.endswith("'")):
                                        self.emit(
                                            "invokevirtual java/lang/StringBuilder/append(Ljava/lang/String;)Ljava/lang/StringBuilder;")
                                    else:
                                        self.emit(
                                            "invokevirtual java/lang/StringBuilder/append(I)Ljava/lang/StringBuilder;")

                                self.emit(
                                    "invokevirtual java/lang/StringBuilder/toString()Ljava/lang/String;")
                                self.emit(
                                    "invokevirtual java/io/PrintStream/println(Ljava/lang/String;)V")
                        else:
                            self.emit(
                                "invokevirtual java/io/PrintStream/println()V")
                        i += 1
                        continue

                    if func_name == "array":
                        self.emit("new java/util/ArrayList")
                        self.emit("dup")
                        self.emit(
                            "invokespecial java/util/ArrayList/<init>()V")
                        i += 1
                        continue

                    if func_name == "read":
                        self.emit("new java/util/Scanner")
                        self.emit("dup")
                        self.emit(
                            "getstatic java/lang/System/in Ljava/io/InputStream;")
                        self.emit(
                            "invokespecial java/util/Scanner/<init>(Ljava/io/InputStream;)V")
                        self.emit("invokevirtual java/util/Scanner/nextInt()I")
                        i += 1
                        continue

                    if func_name == "push":
                        if len(arg_exprs) >= 2:
                            self.visit(arg_exprs[0])
                            self.visit(arg_exprs[1])
                            self.emit(
                                "invokestatic java/lang/Integer/valueOf(I)Ljava/lang/Integer;")
                            self.emit(
                                "invokevirtual java/util/ArrayList/add(Ljava/lang/Object;)Z")
                            self.emit("pop")
                        i += 1
                        continue

                    if func_name == "pop":
                        if len(arg_exprs) >= 1:
                            temp_var = 99
                            self.visit(arg_exprs[0])
                            self.emit("dup")
                            self.emit(
                                "invokevirtual java/util/ArrayList/size()I")
                            self.emit("iconst_1")
                            self.emit("isub")
                            self.emit("dup")
                            self.emit(f"istore {temp_var}")
                            self.emit(
                                "invokevirtual java/util/ArrayList/remove(I)Ljava/lang/Object;")
                            self.emit("checkcast java/lang/Integer")
                            self.emit(
                                "invokevirtual java/lang/Integer/intValue()I")
                        i += 1
                        continue

                    if func_name == "size":
                        if len(arg_exprs) >= 1:
                            self.visit(arg_exprs[0])
                            self.emit(
                                "invokevirtual java/util/ArrayList/size()I")
                        i += 1
                        continue

                    # Função definida pelo usuário
                    func_sym = self.sem.sym.funcs.get(func_name)
                    if func_sym:
                        for expr in arg_exprs:
                            self.visit(expr)
                        param_desc = "".join(self.get_jvm_type(p)
                                             for p in func_sym.param_types)
                        ret_desc = self.get_jvm_type(func_sym.return_type)
                        self.emit(
                            f"invokestatic {self.class_name}/{func_name}({param_desc}){ret_desc}")
                        i += 1
                        continue

            i += 1
