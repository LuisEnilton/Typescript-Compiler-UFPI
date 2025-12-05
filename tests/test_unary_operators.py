"""
Testes de validação de operadores unários (negação e NOT).
Verifica compilação, montagem e execução com saída esperada.
"""

import pytest
import subprocess
import sys
from pathlib import Path
import os


class TestNegativeNumbers:
    """Testes de números negativos"""
    
    @pytest.fixture
    def project_root(self):
        """Retorna o diretório raiz do projeto"""
        return Path(__file__).parent.parent
    
    def test_negative_integer_compiles(self, project_root):
        """Número inteiro negativo deve compilar"""
        code = """let x: number = -5;
print(x);"""
        
        test_file = project_root / "test_negative_int.txt"
        test_file.write_text(code)
        
        result = subprocess.run(
            [sys.executable, str(project_root / "main.py"), str(test_file)],
            capture_output=True,
            text=True,
            cwd=str(project_root)
        )
        
        assert result.returncode == 0, f"Erro compilando: {result.stderr}"
        assert "Semântica concluída sem erros" in result.stdout
        
        test_file.unlink()
    
    def test_negative_integer_execution(self, project_root):
        """Número inteiro negativo deve executar e imprimir corretamente"""
        code = """let x: number = -5;
print(x);"""
        
        test_file = project_root / "test_negative_int.txt"
        test_file.write_text(code)
        
        # Compila
        subprocess.run(
            [sys.executable, str(project_root / "main.py"), str(test_file)],
            capture_output=True,
            text=True,
            cwd=str(project_root)
        )
        
        # Monta com Jasmin
        result = subprocess.run(
            ["java", "-jar", str(project_root / "jasmin.jar"), 
             str(project_root / "Test_negative_int.j")],
            capture_output=True,
            text=True,
            cwd=str(project_root)
        )
        assert result.returncode == 0, f"Erro montando: {result.stderr}"
        
        # Executa
        result = subprocess.run(
            ["java", "Test_negative_int"],
            capture_output=True,
            text=True,
            cwd=str(project_root),
            timeout=10
        )
        
        assert result.returncode == 0, f"Erro executando: {result.stderr}"
        assert "-5" in result.stdout, f"Esperado '-5' na saída, obteve: {result.stdout}"
        
        test_file.unlink()
    
    def test_negative_variable(self, project_root):
        """Negação de variável deve funcionar"""
        code = """let x: number = 10;
let y: number = -x;
print(y);"""
        
        test_file = project_root / "test_neg_var.txt"
        test_file.write_text(code)
        
        # Compila
        subprocess.run(
            [sys.executable, str(project_root / "main.py"), str(test_file)],
            capture_output=True,
            text=True,
            cwd=str(project_root)
        )
        
        # Monta com Jasmin
        result = subprocess.run(
            ["java", "-jar", str(project_root / "jasmin.jar"), 
             str(project_root / "Test_neg_var.j")],
            capture_output=True,
            text=True,
            cwd=str(project_root)
        )
        assert result.returncode == 0
        
        # Executa
        result = subprocess.run(
            ["java", "Test_neg_var"],
            capture_output=True,
            text=True,
            cwd=str(project_root),
            timeout=10
        )
        
        assert result.returncode == 0
        assert "-10" in result.stdout, f"Esperado '-10', obteve: {result.stdout}"
        
        test_file.unlink()
    
    def test_double_negation(self, project_root):
        """Dupla negação deve resultar no valor positivo"""
        code = """let x: number = --5;
print(x);"""
        
        test_file = project_root / "test_double_neg.txt"
        test_file.write_text(code)
        
        # Compila
        subprocess.run(
            [sys.executable, str(project_root / "main.py"), str(test_file)],
            capture_output=True,
            text=True,
            cwd=str(project_root)
        )
        
        # Monta com Jasmin
        result = subprocess.run(
            ["java", "-jar", str(project_root / "jasmin.jar"), 
             str(project_root / "Test_double_neg.j")],
            capture_output=True,
            text=True,
            cwd=str(project_root)
        )
        assert result.returncode == 0
        
        # Executa
        result = subprocess.run(
            ["java", "Test_double_neg"],
            capture_output=True,
            text=True,
            cwd=str(project_root),
            timeout=10
        )
        
        assert result.returncode == 0
        assert "5" in result.stdout, f"Esperado '5', obteve: {result.stdout}"
        
        test_file.unlink()
    
    def test_negative_expression(self, project_root):
        """Negação de expressão deve funcionar"""
        code = """let a: number = 10;
let b: number = 5;
let c: number = -(a + b);
print(c);"""
        
        test_file = project_root / "test_neg_expr.txt"
        test_file.write_text(code)
        
        # Compila
        subprocess.run(
            [sys.executable, str(project_root / "main.py"), str(test_file)],
            capture_output=True,
            text=True,
            cwd=str(project_root)
        )
        
        # Monta com Jasmin
        result = subprocess.run(
            ["java", "-jar", str(project_root / "jasmin.jar"), 
             str(project_root / "Test_neg_expr.j")],
            capture_output=True,
            text=True,
            cwd=str(project_root)
        )
        assert result.returncode == 0
        
        # Executa
        result = subprocess.run(
            ["java", "Test_neg_expr"],
            capture_output=True,
            text=True,
            cwd=str(project_root),
            timeout=10
        )
        
        assert result.returncode == 0
        assert "-15" in result.stdout, f"Esperado '-15', obteve: {result.stdout}"
        
        test_file.unlink()


class TestLogicalNot:
    """Testes de operador NOT lógico"""
    
    @pytest.fixture
    def project_root(self):
        """Retorna o diretório raiz do projeto"""
        return Path(__file__).parent.parent
    
    def test_logical_not_true(self, project_root):
        """NOT de true deve ser false (0)"""
        code = """let x: boolean = !true;
print(x);"""
        
        test_file = project_root / "test_not_true.txt"
        test_file.write_text(code)
        
        # Compila
        subprocess.run(
            [sys.executable, str(project_root / "main.py"), str(test_file)],
            capture_output=True,
            text=True,
            cwd=str(project_root)
        )
        
        # Monta com Jasmin
        result = subprocess.run(
            ["java", "-jar", str(project_root / "jasmin.jar"), 
             str(project_root / "Test_not_true.j")],
            capture_output=True,
            text=True,
            cwd=str(project_root)
        )
        assert result.returncode == 0
        
        # Executa
        result = subprocess.run(
            ["java", "Test_not_true"],
            capture_output=True,
            text=True,
            cwd=str(project_root),
            timeout=10
        )
        
        assert result.returncode == 0
        # false é representado como 0
        assert "0" in result.stdout, f"Esperado '0' para false, obteve: {result.stdout}"
        
        test_file.unlink()
    
    def test_logical_not_false(self, project_root):
        """NOT de false deve ser true (1)"""
        code = """let x: boolean = !false;
print(x);"""
        
        test_file = project_root / "test_not_false.txt"
        test_file.write_text(code)
        
        # Compila
        subprocess.run(
            [sys.executable, str(project_root / "main.py"), str(test_file)],
            capture_output=True,
            text=True,
            cwd=str(project_root)
        )
        
        # Monta com Jasmin
        result = subprocess.run(
            ["java", "-jar", str(project_root / "jasmin.jar"), 
             str(project_root / "Test_not_false.j")],
            capture_output=True,
            text=True,
            cwd=str(project_root)
        )
        assert result.returncode == 0
        
        # Executa
        result = subprocess.run(
            ["java", "Test_not_false"],
            capture_output=True,
            text=True,
            cwd=str(project_root),
            timeout=10
        )
        
        assert result.returncode == 0
        # true é representado como 1
        assert "1" in result.stdout, f"Esperado '1' para true, obteve: {result.stdout}"
        
        test_file.unlink()
    
    def test_logical_not_number_zero(self, project_root):
        """NOT de zero deve ser true (1)"""
        code = """let x: number = 0;
let y: boolean = !x;
print(y);"""
        
        test_file = project_root / "test_not_zero.txt"
        test_file.write_text(code)
        
        # Compila
        subprocess.run(
            [sys.executable, str(project_root / "main.py"), str(test_file)],
            capture_output=True,
            text=True,
            cwd=str(project_root)
        )
        
        # Monta com Jasmin
        result = subprocess.run(
            ["java", "-jar", str(project_root / "jasmin.jar"), 
             str(project_root / "Test_not_zero.j")],
            capture_output=True,
            text=True,
            cwd=str(project_root)
        )
        assert result.returncode == 0
        
        # Executa
        result = subprocess.run(
            ["java", "Test_not_zero"],
            capture_output=True,
            text=True,
            cwd=str(project_root),
            timeout=10
        )
        
        assert result.returncode == 0
        assert "1" in result.stdout, f"Esperado '1', obteve: {result.stdout}"
        
        test_file.unlink()
    
    def test_logical_not_number_nonzero(self, project_root):
        """NOT de número não-zero deve ser false (0)"""
        code = """let x: number = 5;
let y: boolean = !x;
print(y);"""
        
        test_file = project_root / "test_not_nonzero.txt"
        test_file.write_text(code)
        
        # Compila
        subprocess.run(
            [sys.executable, str(project_root / "main.py"), str(test_file)],
            capture_output=True,
            text=True,
            cwd=str(project_root)
        )
        
        # Monta com Jasmin
        result = subprocess.run(
            ["java", "-jar", str(project_root / "jasmin.jar"), 
             str(project_root / "Test_not_nonzero.j")],
            capture_output=True,
            text=True,
            cwd=str(project_root)
        )
        assert result.returncode == 0
        
        # Executa
        result = subprocess.run(
            ["java", "Test_not_nonzero"],
            capture_output=True,
            text=True,
            cwd=str(project_root),
            timeout=10
        )
        
        assert result.returncode == 0
        assert "0" in result.stdout, f"Esperado '0', obteve: {result.stdout}"
        
        test_file.unlink()
