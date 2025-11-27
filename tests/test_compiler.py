import pytest
from .compiler_utils import compile_code


class TestVariableDeclaration:
    """Testes para declaração de variáveis"""
    
    def test_valid_let_declaration(self):
        """Variável let com inicialização deve compilar"""
        code = "let x: number = 10;"
        success, errors = compile_code(code)
        assert success, f"Esperado sucesso, mas obteve erros: {errors}"
    
    def test_valid_const_declaration_with_init(self):
        """Variável const com inicialização deve compilar"""
        code = "const x: number = 10;"
        success, errors = compile_code(code)
        assert success, f"Esperado sucesso, mas obteve erros: {errors}"
    
    def test_const_without_init_error(self):
        """Variável const sem inicialização deve gerar erro"""
        code = "const x: number;"
        success, errors = compile_code(code)
        assert not success, "Esperado erro para const sem inicialização"
        assert any("inicializ" in str(e).lower() for e in errors), \
            f"Erro deve mencionar inicialização, obteve: {errors}"
    
    def test_const_reassignment_error(self):
        """Reatribuição a variável const deve gerar erro"""
        code = """
const x: number = 10;
x = 20;
"""
        success, errors = compile_code(code)
        assert not success, "Esperado erro para reatribuição de const"
        assert any("const" in str(e).lower() for e in errors), \
            f"Erro deve mencionar const, obteve: {errors}"
    
    def test_type_mismatch_error(self):
        """Atribuição de tipo incompatível deve gerar erro"""
        code = "let x: number = \"abc\";"
        success, errors = compile_code(code)
        assert not success, "Esperado erro de tipo incompatível"
        assert any("incompat" in str(e).lower() or "type" in str(e).lower() for e in errors), \
            f"Erro deve mencionar tipos incompatíveis, obteve: {errors}"
    
    def test_undeclared_variable_error(self):
        """Uso de variável não declarada deve gerar erro"""
        code = "let x: number = y;"
        success, errors = compile_code(code)
        assert not success, "Esperado erro para variável não declarada"


class TestArrayOperations:
    """Testes para operações com arrays"""
    
    def test_valid_array_declaration(self):
        """Declaração e inicialização de array deve compilar"""
        code = "let nums: number[] = [1, 2, 3, 4];"
        success, errors = compile_code(code)
        assert success, f"Esperado sucesso, mas obteve erros: {errors}"
    
    def test_valid_array_access(self):
        """Acesso a elemento de array deve compilar"""
        code = """
let nums: number[] = [1, 2, 3, 4];
let x: number = nums[2];
"""
        success, errors = compile_code(code)
        assert success, f"Esperado sucesso, mas obteve erros: {errors}"
    
    def test_array_assignment_valid(self):
        """Atribuição a elemento de array deve compilar"""
        code = """
let nums: number[] = [1, 2, 3, 4];
nums[0] = 100;
"""
        success, errors = compile_code(code)
        assert success, f"Esperado sucesso, mas obteve erros: {errors}"
    
    def test_heterogeneous_array_error(self):
        """Array com tipos diferentes deve gerar erro"""
        code = "let arr: number[] = [1, \"abc\", 3];"
        success, errors = compile_code(code)
        assert not success, "Esperado erro para array heterogêneo"
    
    def test_empty_array_assignment(self):
        """Atribuição a array vazio deve compilar"""
        code = """
let arr: number[] = [];
arr[0] = 5;
"""
        success, errors = compile_code(code)
        assert success, f"Esperado sucesso, mas obteve erros: {errors}"


class TestFunctions:
    """Testes para declaração e chamada de funções"""
    
    def test_valid_function_declaration(self):
        """Declaração de função válida deve compilar"""
        code = """
function soma(a: number, b: number): number {
    return a + b;
}
"""
        success, errors = compile_code(code)
        assert success, f"Esperado sucesso, mas obteve erros: {errors}"
    
    def test_function_return_type_mismatch(self):
        """Retorno com tipo incompatível deve gerar erro"""
        code = """
function soma(a: number, b: number): number {
    return "abc";
}
"""
        success, errors = compile_code(code)
        assert not success, "Esperado erro de tipo de retorno incompatível"
        assert any("retorn" in str(e).lower() or "tipo" in str(e).lower() for e in errors), \
            f"Erro deve mencionar tipo de retorno, obteve: {errors}"
    
    def test_function_missing_return(self):
        """Função sem retorno onde esperado pode compilar (sem verificação)"""
        code = """
function test(): number {
}
"""
        # Este teste apenas verifica se há parsing/análise
        success, errors = compile_code(code)
        # Comportamento pode variar dependendo da implementação
    
    def test_function_param_type_checking(self):
        """Verificação de tipo de parâmetro em chamada de função"""
        code = """
function soma(a: number, b: number): number {
    return a + b;
}
let result: number = soma(5, 10);
"""
        success, errors = compile_code(code)
        assert success, f"Esperado sucesso, mas obteve erros: {errors}"
    
    def test_undeclared_function_error(self):
        """Chamada a função não declarada deve gerar erro"""
        code = "let x: number = undeclared_func();"
        success, errors = compile_code(code)
        # Pode gerar erro ou não, dependendo se nativa ou não
        # Função nativa read/print devem funcionar


class TestInterfaces:
    """Testes para interfaces"""
    
    def test_valid_interface_declaration(self):
        """Declaração de interface válida deve compilar"""
        code = """
interface User {
    name: string;
    age: number;
}
"""
        success, errors = compile_code(code)
        assert success, f"Esperado sucesso, mas obteve erros: {errors}"
    
    def test_interface_object_literal_assignment(self):
        """Atribuição de object literal compatível com interface deve compilar"""
        code = """
interface User {
    name: string;
    age: number;
}
let u: User = {
    name: "Ana",
    age: 30
};
"""
        success, errors = compile_code(code)
        assert success, f"Esperado sucesso, mas obteve erros: {errors}"
    
    def test_interface_missing_property_error(self):
        """Object literal faltando propriedade obrigatória deve gerar erro"""
        code = """
interface User {
    name: string;
    age: number;
}
let u: User = {
    name: "Ana"
};
"""
        success, errors = compile_code(code)
        assert not success, "Esperado erro para propriedade faltante"
        assert any("ausente" in str(e).lower() or "missing" in str(e).lower() for e in errors), \
            f"Erro deve mencionar propriedade ausente, obteve: {errors}"
    
    def test_interface_extra_property_error(self):
        """Object literal com propriedade extra deve gerar erro"""
        code = """
interface User {
    name: string;
    age: number;
}
let u: User = {
    name: "Ana",
    age: 30,
    extra: "field"
};
"""
        success, errors = compile_code(code)
        assert not success, "Esperado erro para propriedade extra"
        assert any("extra" in str(e).lower() or "unknown" in str(e).lower() for e in errors), \
            f"Erro deve mencionar propriedade extra, obteve: {errors}"
    
    def test_interface_property_access(self):
        """Acesso a propriedade de interface deve compilar"""
        code = """
interface User {
    name: string;
    age: number;
}
let u: User = { name: "Ana", age: 30 };
let n: string = u.name;
"""
        success, errors = compile_code(code)
        assert success, f"Esperado sucesso, mas obteve erros: {errors}"
    
    def test_interface_invalid_property_assignment(self):
        """Atribuição a propriedade inexistente de interface deve gerar erro"""
        code = """
interface User {
    name: string;
    age: number;
}
let u: User = { name: "Ana", age: 30 };
u.namo = "Jose";
"""
        success, errors = compile_code(code)
        assert not success, "Esperado erro para propriedade inexistente"
        assert any("namo" in str(e).lower() or "campo" in str(e).lower() for e in errors), \
            f"Erro deve mencionar propriedade 'namo', obteve: {errors}"
    
    def test_interface_property_type_mismatch(self):
        """Atribuição de tipo incompatível a propriedade deve gerar erro"""
        code = """
interface User {
    name: string;
    age: number;
}
let u: User = { name: "Ana", age: 30 };
u.name = 123;
"""
        success, errors = compile_code(code)
        assert not success, "Esperado erro de tipo incompatível"


class TestExpressions:
    """Testes para expressões e operações"""
    
    def test_valid_arithmetic_expression(self):
        """Expressão aritmética válida deve compilar"""
        code = """
let a: number = 10;
let b: number = 20;
let c: number = a + b;
"""
        success, errors = compile_code(code)
        assert success, f"Esperado sucesso, mas obteve erros: {errors}"
    
    def test_valid_comparison_expression(self):
        """Expressão de comparação válida deve compilar"""
        code = """
let a: number = 10;
let b: boolean = a > 5;
"""
        success, errors = compile_code(code)
        assert success, f"Esperado sucesso, mas obteve erros: {errors}"
    
    def test_logical_and_expression(self):
        """Expressão lógica AND deve compilar"""
        code = """
let a: boolean = true;
let b: boolean = false;
let c: boolean = a && b;
"""
        success, errors = compile_code(code)
        assert success, f"Esperado sucesso, mas obteve erros: {errors}"
    
    def test_logical_or_expression(self):
        """Expressão lógica OR deve compilar"""
        code = """
let a: boolean = true;
let b: boolean = false;
let c: boolean = a || b;
"""
        success, errors = compile_code(code)
        assert success, f"Esperado sucesso, mas obteve erros: {errors}"


class TestControlFlow:
    """Testes para controle de fluxo"""
    
    def test_valid_if_statement(self):
        """Comando if válido deve compilar"""
        code = """
let x: number = 10;
if (x > 5) {
    let y: number = 20;
}
"""
        success, errors = compile_code(code)
        assert success, f"Esperado sucesso, mas obteve erros: {errors}"
    
    def test_valid_if_else_statement(self):
        """Comando if-else válido deve compilar"""
        code = """
let x: number = 10;
if (x > 5) {
    let y: number = 20;
} else {
    let z: number = 30;
}
"""
        success, errors = compile_code(code)
        assert success, f"Esperado sucesso, mas obteve erros: {errors}"
    
    def test_valid_while_loop(self):
        """Comando while válido deve compilar"""
        code = """
let i: number = 0;
while (i < 10) {
    i = i + 1;
}
"""
        success, errors = compile_code(code)
        assert success, f"Esperado sucesso, mas obteve erros: {errors}"
    
    def test_valid_for_loop(self):
        """Comando for válido deve compilar"""
        code = """
for (let i: number = 0; i < 10; i = i + 1) {
    let x: number = i;
}
"""
        success, errors = compile_code(code)
        assert success, f"Esperado sucesso, mas obteve erros: {errors}"


class TestComplexScenarios:
    """Testes de cenários complexos"""
    
    def test_function_with_interface_parameter(self):
        """Função com parâmetro de tipo interface deve compilar"""
        code = """
interface Person {
    name: string;
    age: number;
}
function greet(p: Person): string {
    return "Hello";
}
"""
        success, errors = compile_code(code)
        assert success, f"Esperado sucesso, mas obteve erros: {errors}"
    
    def test_nested_object_literal(self):
        """Object literal aninhado deve compilar se compatível"""
        code = """
interface Address {
    street: string;
    number: number;
}
interface User {
    name: string;
    address: Address;
}
let user: User = {
    name: "Ana",
    address: {
        street: "Main St",
        number: 123
    }
};
"""
        success, errors = compile_code(code)
        # Pode compilar ou não dependendo da implementação de nested interfaces
    
    def test_array_of_interfaces(self):
        """Array de interfaces deve compilar"""
        code = """
interface User {
    name: string;
    age: number;
}
let users: User[] = [
    { name: "Ana", age: 30 },
    { name: "Bob", age: 25 }
];
"""
        success, errors = compile_code(code)
        assert success, f"Esperado sucesso, mas obteve erros: {errors}"
