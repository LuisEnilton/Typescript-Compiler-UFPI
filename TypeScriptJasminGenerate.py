from antlr4 import ParseTreeVisitor
from TypeScriptParser import TypeScriptParser
# Importamos as classes de tipo do seu analisador semântico para referência
from TypeScriptSemantic import PrimitiveType, ArrayType, InterfaceType


class JasminGenerator(ParseTreeVisitor):
    def __init__(self, semantic_analyzer, class_name="Output"):
        self.sem = semantic_analyzer
        self.class_name = class_name
        self.code = []  # Lista para armazenar as linhas do código Jasmin
        self.interface_classes = []  # Código das classes de interface geradas

        # Controle de Labels e Locals
        self.label_counter = 0
        self.local_var_index = 0
        self.local_vars = {}  # Mapa {nome: indice_jvm} para o escopo atual
        self.local_var_types = {}  # Mapa {nome: tipo} para rastrear tipos de variáveis locais
        self.in_main_method = False  # Flag para rastrear se estamos no main
        self.in_expression_stmt = False  # Flag para rastrear se estamos em um expression statement

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

    def _find_var_symbol(self, name):
        """Encontra um símbolo de variável (local ou global)"""
        # Primeiro verifica local_var_types
        if name in self.local_var_types:
            class DummySymbol:
                pass
            sym = DummySymbol()
            sym.type = self.local_var_types[name]
            return sym
        # Depois verifica global_vars
        if name in self.sem.sym.global_vars:
            return self.sem.sym.global_vars[name]
        return None

    def _infer_expr_type(self, expr_ctx):
        """Infere o tipo de uma expressão baseado em seu texto/contexto"""
        expr_text = expr_ctx.getText()
        
        # String literal
        if (expr_text.startswith('"') and expr_text.endswith('"')) or \
           (expr_text.startswith("'") and expr_text.endswith("'")):
            return "string"
        
        # Number literal
        if expr_text.isdigit():
            return "number"
        
        # Field access: obj.field
        if '.' in expr_text:
            parts = expr_text.split('.')
            if len(parts) >= 2:
                var_name = parts[0]
                field_name = parts[-1]
                
                # Procura a variável para determinar seu tipo
                var_symbol = self._find_var_symbol(var_name)
                if var_symbol and hasattr(var_symbol, 'type'):
                    var_type = var_symbol.type
                    if isinstance(var_type, InterfaceType):
                        # Busca tipo do field na interface
                        if field_name in var_type.props:
                            field_type = var_type.props[field_name]
                            if isinstance(field_type, PrimitiveType):
                                return field_type.name()
                            return "object"
        
        # Variável simples
        var_symbol = self._find_var_symbol(expr_text)
        if var_symbol and hasattr(var_symbol, 'type'):
            var_type = var_symbol.type
            if isinstance(var_type, PrimitiveType):
                return var_type.name()
        
        # Default: assume number
        return "number"

    def _get_array_element_type(self, array_var_name):
        """Retorna o tipo do elemento de um array"""
        var_symbol = self._find_var_symbol(array_var_name)
        
        if var_symbol and hasattr(var_symbol, 'type'):
            var_type = var_symbol.type
            if isinstance(var_type, ArrayType):
                elem_type = var_type.elem
                if isinstance(elem_type, PrimitiveType):
                    return elem_type.name()
                elif isinstance(elem_type, InterfaceType):
                    return f"interface:{elem_type.name()}"
        
        return "unknown"

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
        if isinstance(ts_type, InterfaceType):
            # Interface é um objeto de sua própria classe
            return f"L{ts_type.name()};"
        # Default/Fallback
        return "I"

    def get_result(self):
        """Retorna o código Jasmin completo (apenas da classe principal, sem interfaces)"""
        # Retorna apenas o código da classe principal
        return "\n".join(self.code)

    def generate_interface_classes(self):
        """Gera classes Java para todas as interfaces definidas"""
        for iface_name, iface_type in self.sem.sym.interfaces.items():
            class_code = []
            class_code.append(f".class public {iface_name}")
            class_code.append(".super java/lang/Object")
            class_code.append("")
            
            # Fields para cada propriedade da interface
            for prop_name, prop_type in iface_type.props.items():
                desc = self.get_jvm_type(prop_type)
                class_code.append(f".field public {prop_name} {desc}")
            
            class_code.append("")
            
            # Construtor padrão
            class_code.append(".method public <init>()V")
            class_code.append("    aload_0")
            class_code.append("    invokespecial java/lang/Object/<init>()V")
            class_code.append("    return")
            class_code.append(".end method")
            class_code.append("")
            
            self.interface_classes.append("\n".join(class_code))

    # ========================================================================
    # VISITORS PRINCIPAIS
    # ========================================================================

    def visitProgram(self, ctx: TypeScriptParser.ProgramContext):
        # Primeiro: Gerar classes de interface
        self.generate_interface_classes()
        
        # Cabeçalho da Classe Principal
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
        self.in_main_method = True  # Set flag para main

        for child in ctx.children:
            if isinstance(child, TypeScriptParser.StatementContext):
                # Processa todos os statements globais (incluindo declarações de variáveis)
                # que precisam ser inicializadas em runtime
                if not child.functionDecl() and not child.interfaceDecl():
                    self.visit(child)

        self.in_main_method = False  # Reset flag
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
        
        # Primeiro, obtém o tipo da variável do contexto
        parsed_type = None
        if ctx.typeExpr():
            parsed_type = self.sem.type_from_ctx(ctx.typeExpr())

        # Se tem inicialização (ex: let x = 10)
        if ctx.expression():
            # 1. Gera código da expressão (deixa valor na pilha)
            self.visit(ctx.expression())

            # 2. Armazena o valor
            if name in self.local_vars:
                # É reatribuição de variável local existente
                idx = self.local_vars[name]
                
                # Verifica se precisa fazer cast
                if parsed_type and isinstance(parsed_type, InterfaceType):
                    iface_name = parsed_type.name()
                    self.emit(f"checkcast {iface_name}")
                    self.emit(f"astore {idx}")
                elif parsed_type and isinstance(parsed_type, ArrayType):
                    self.emit(f"astore {idx}")
                else:
                    # Primitivo
                    expr_text = ctx.expression().getText() if ctx.expression() else ""
                    if expr_text.startswith("array("):
                        self.emit(f"astore {idx}")
                    else:
                        self.emit(f"istore {idx}")
            elif name in self.sem.sym.global_vars and not self.in_main_method:
                # É uma variável global (declarada no nível superior do programa, fora do main)
                var_sym = self.sem.sym.global_vars[name]
                desc = self.get_jvm_type(var_sym.type)
                self.emit("dup")
                self.emit(f"putstatic {self.class_name}/{name} {desc}")
            else:
                # Nova variável local dentro de um método
                idx = self.local_var_index
                self.local_vars[name] = idx
                self.local_var_index += 1
                
                # Armazena tipo da variável
                if parsed_type:
                    self.local_var_types[name] = parsed_type

                # Check type for correct store instruction
                if parsed_type:
                    if isinstance(parsed_type, InterfaceType):
                        # Se é interface, precisa fazer cast do Object retornado de array access
                        iface_name = parsed_type.name()
                        self.emit(f"checkcast {iface_name}")
                        self.emit(f"astore {idx}")
                    elif isinstance(parsed_type, ArrayType):
                        self.emit(f"astore {idx}")
                    else:
                        self.emit(f"istore {idx}")  # Use istore para primitivos
                else:
                    # Fallback - tenta detectar pelo texto da expressão
                    expr_text = ctx.expression().getText() if ctx.expression() else ""
                    if expr_text.startswith("array("):
                        self.emit(f"astore {idx}")
                    else:
                        self.emit(f"istore {idx}")
        else:
            # Sem inicialização - precisa instanciar se for interface
            # Se for variável de interface sem inicializador
            if parsed_type and isinstance(parsed_type, InterfaceType):
                # Cria instância: new NomeDaInterface(); dup(); invokespecial <init>()V
                iface_name = parsed_type.name()
                self.emit(f"new {iface_name}")
                self.emit("dup")
                self.emit(f"invokespecial {iface_name}/<init>()V")
                self.emit(f"putstatic {self.class_name}/{name} L{iface_name};")
            else:
                # Para local variables sem inicializador, registra apenas
                if name not in self.local_vars:
                    idx = self.local_var_index
                    self.local_vars[name] = idx
                    self.local_var_index += 1
                    # Armazena tipo
                    if parsed_type:
                        self.local_var_types[name] = parsed_type

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
        # Atribuições a campo (obj.campo = ...) também não deixam valor na pilha (putfield consome)
        is_void_func = (expr_text.startswith("print(") or
                        expr_text.startswith("push(") or
                        ".push(" in expr_text or
                        ("=" in expr_text and "." in expr_text))  # Atribuição a campo

        self.visit(expr_ctx)

        # Se não é função void e não é atribuição a campo, há um valor na pilha que precisa ser descartado
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
        # Se tem atribuição (ex: x = 10 ou obj.campo = 10)
        if ctx.ASSIGN():
            # Lado direito (valor)
            self.visit(ctx.assignmentExpr())

            # Lado esquerdo (variável ou campo)
            left_text = ctx.getChild(0).getText()
            
            # Verifica se é atribuição a campo (ex: obj.campo)
            if '.' in left_text:
                # Atribuição a campo de interface
                parts = left_text.split('.')
                if len(parts) == 2:
                    obj_name = parts[0]
                    field_name = parts[1]
                    
                    # Obtém tipo do campo e tipo do objeto
                    obj_sym = self._find_var_symbol(obj_name)
                    if obj_sym and isinstance(obj_sym.type, InterfaceType):
                        iface_name = obj_sym.type.name()
                        iface_type = self.sem.sym.interfaces.get(iface_name)
                        
                        # Obtém o objeto (antes de colocar na pilha)
                        if obj_name in self.local_vars:
                            idx = self.local_vars[obj_name]
                            # Pilha: [valor]
                            # Queremos: [objeto, valor] para putfield
                            self.emit(f"aload {idx}")  # Pilha: [valor, objeto]
                            self.emit("swap")  # Pilha: [objeto, valor]
                        elif obj_name in self.sem.sym.global_vars:
                            desc = self.get_jvm_type(obj_sym.type)
                            # Pilha: [valor]
                            self.emit(f"getstatic {self.class_name}/{obj_name} {desc}")  # Pilha: [valor, objeto]
                            self.emit("swap")  # Pilha: [objeto, valor]
                        
                        if iface_type and field_name in iface_type.props:
                            field_type = iface_type.props[field_name]
                            desc = self.get_jvm_type(field_type)
                            self.emit(f"putfield {iface_name}/{field_name} {desc}")
                            # putfield não deixa nada na pilha
            else:
                # Atribuição simples a variável
                var_name = left_text
                
                if var_name in self.local_vars:
                    idx = self.local_vars[var_name]
                    # Mantém valor na pilha para encadeamento (a = b = c)
                    self.emit("dup")
                    # Verifica se é interface ou primitivo
                    var_sym = self._find_var_symbol(var_name)
                    if var_sym and isinstance(var_sym.type, InterfaceType):
                        self.emit(f"astore {idx}")
                    else:
                        self.emit(f"istore {idx}")
                elif var_name in self.sem.sym.global_vars:
                    var_sym = self.sem.sym.global_vars[var_name]
                    desc = self.get_jvm_type(var_sym.type)
                    self.emit("dup")
                    self.emit(f"putstatic {self.class_name}/{var_name} {desc}")
                    # Deixa um valor na pilha para encadeamento
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

    def visitUnaryExpr(self, ctx: TypeScriptParser.UnaryExprContext):
        # unaryExpr: (NOT | MINUS)* postfixExpr;
        # Conta quantos operadores unários temos
        operator_count = 0
        minus_count = 0
        not_count = 0
        
        for i in range(ctx.getChildCount()):
            child_text = ctx.getChild(i).getText()
            if child_text == '-':
                minus_count += 1
                operator_count += 1
            elif child_text == '!':
                not_count += 1
                operator_count += 1
        
        # Se não há operadores unários, apenas visita postfixExpr
        if operator_count == 0:
            self.visit(ctx.postfixExpr())
            return
        
        # Visita o operand (postfixExpr)
        self.visit(ctx.postfixExpr())
        
        # Aplica os operadores unários de trás para frente (negação múltipla)
        # Por exemplo: --x é o mesmo que x (duas negações)
        # -x é negação simples
        
        # Aplica negações (MINUS)
        if minus_count > 0:
            # Número ímpar de negações resulta em uma negação
            if minus_count % 2 == 1:
                self.emit("ineg")
        
        # Aplica NOT lógico (!x)
        if not_count > 0:
            # Número ímpar de NOT resulta em NOT
            if not_count % 2 == 1:
                # NOT lógico: !x
                # Se x != 0, resultado = 0
                # Se x == 0, resultado = 1
                true_label = self.get_new_label()
                end_label = self.get_new_label()
                
                self.emit(f"ifeq {true_label}")
                self.emit("iconst_0")  # x != 0 -> !x = 0
                self.emit(f"goto {end_label}")
                self.emit_label(true_label)
                self.emit("iconst_1")  # x == 0 -> !x = 1
                self.emit_label(end_label)

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
                # Verifica se é interface ou array (referências)
                var_type = self.local_var_types.get(name)
                if var_type and isinstance(var_type, (InterfaceType, ArrayType)):
                    self.emit(f"aload {idx}")
                else:
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
                # Obtém o nome do array (primary)
                primary_text = primary.getText()
                array_elem_type = self._get_array_element_type(primary_text)
                
                if hasattr(op, 'expression') and op.expression():
                    self.visit(op.expression()[0])
                
                self.emit(
                    "invokevirtual java/util/ArrayList/get(I)Ljava/lang/Object;")
                
                # Converte Object para o tipo correto
                if array_elem_type == "number":
                    # Array de numbers: unbox Integer
                    self.emit("checkcast java/lang/Integer")
                    self.emit("invokevirtual java/lang/Integer/intValue()I")
                elif array_elem_type.startswith("interface:"):
                    # Array de interfaces: faz checkcast
                    iface_name = array_elem_type.split(':')[1]
                    self.emit(f"checkcast {iface_name}")
                elif array_elem_type == "string":
                    # Array de strings: faz checkcast
                    self.emit("checkcast java/lang/String")
                # else: deixa como Object
                
                i += 1
                continue

            # Métodos de array e acesso a campos de interface
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
                        # Verifica o tipo do argumento para determinar se precisa converter
                        arg_text = arg_exprs[0].getText()
                        arg_sym = None
                        if arg_text in self.sem.sym.global_vars:
                            arg_sym = self.sem.sym.global_vars[arg_text]
                        
                        # Se não é interface, converte para Integer
                        if arg_sym is None or not isinstance(arg_sym.type, InterfaceType):
                            self.emit(
                                "invokestatic java/lang/Integer/valueOf(I)Ljava/lang/Integer;")
                        # Se for interface, já está como Object na pilha, pode adicionar direto
                        
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
                
                # Acesso a campo de interface (ex: obj.campo)
                if not (next_op and next_op.getText().startswith('(')):
                    # É acesso a campo, não método
                    # Obtém o tipo do objeto principal
                    primary_name = primary.ID().getText() if primary.ID() else None
                    if primary_name:
                        primary_sym = self._find_var_symbol(primary_name)
                        if primary_sym and isinstance(primary_sym.type, InterfaceType):
                            iface_name = primary_sym.type.name()
                            # Acesso ao campo: getfield NomeDaInterface/campo tipo
                            iface_type = self.sem.sym.interfaces.get(iface_name)
                            if iface_type and method_name in iface_type.props:
                                field_type = iface_type.props[method_name]
                                desc = self.get_jvm_type(field_type)
                                self.emit(f"getfield {iface_name}/{method_name} {desc}")
                                result_type = field_type
                    i += 1
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
                                    
                                    # Determina o tipo real do argumento
                                    arg_type = self._infer_expr_type(arg)
                                    
                                    if arg_type == "string":
                                        self.emit(
                                            "invokevirtual java/lang/StringBuilder/append(Ljava/lang/String;)Ljava/lang/StringBuilder;")
                                    else:
                                        # number ou outros tipos
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
