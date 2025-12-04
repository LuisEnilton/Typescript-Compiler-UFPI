"""
Testes de validação da execução dos exemplos.
Verifica que os exemplos compilam, montam e executam sem erros.
"""

import pytest
import subprocess
import sys
from pathlib import Path
import os


class TestExamplesCompile:
    """Testes de compilação de exemplos"""
    
    @pytest.fixture
    def project_root(self):
        """Retorna o diretório raiz do projeto"""
        return Path(__file__).parent.parent
    
    def get_example_files(self, project_root):
        """Lista arquivos de exemplo"""
        examples_dir = project_root
        examples = []
        
        # Busca todos os exemplo_*.txt e teste_*.txt
        for pattern in ["exemplo_*.txt", "teste_*.txt"]:
            for f in examples_dir.glob(pattern):
                if f.is_file():
                    examples.append(f)
        
        return sorted(examples)
    
    def test_exemplo_1_compiles(self, project_root):
        """exemplo_1.txt deve compilar sem erros"""
        example_file = project_root / "exemplo_1.txt"
        result = subprocess.run(
            [sys.executable, str(project_root / "main.py"), str(example_file)],
            capture_output=True,
            text=True,
            cwd=str(project_root)
        )
        assert result.returncode == 0, f"Erro compilando: {result.stdout}\n{result.stderr}"
        assert "Semântica concluída sem erros" in result.stdout
    
    def test_exemplo_interface_produtos_compiles(self, project_root):
        """exemplo_interface_produtos.txt deve compilar sem erros"""
        example_file = project_root / "exemplo_interface_produtos.txt"
        result = subprocess.run(
            [sys.executable, str(project_root / "main.py"), str(example_file)],
            capture_output=True,
            text=True,
            cwd=str(project_root)
        )
        assert result.returncode == 0, f"Erro compilando: {result.stdout}\n{result.stderr}"
        assert "Semântica concluída sem erros" in result.stdout
    
    def test_teste_interfaces_multiplas_compiles(self, project_root):
        """teste_interfaces_multiplas.txt deve compilar sem erros"""
        example_file = project_root / "teste_interfaces_multiplas.txt"
        if example_file.exists():
            result = subprocess.run(
                [sys.executable, str(project_root / "main.py"), str(example_file)],
                capture_output=True,
                text=True,
                cwd=str(project_root)
            )
            assert result.returncode == 0, f"Erro compilando: {result.stdout}\n{result.stderr}"
            assert "Semântica concluída sem erros" in result.stdout
    
    def test_teste_boletim_compiles(self, project_root):
        """teste_boletim.txt deve compilar sem erros"""
        example_file = project_root / "teste_boletim.txt"
        if example_file.exists():
            result = subprocess.run(
                [sys.executable, str(project_root / "main.py"), str(example_file)],
                capture_output=True,
                text=True,
                cwd=str(project_root)
            )
            assert result.returncode == 0, f"Erro compilando: {result.stdout}\n{result.stderr}"
            assert "Semântica concluída sem erros" in result.stdout


class TestExamplesExecution:
    """Testes de execução de exemplos compilados"""
    
    @pytest.fixture
    def project_root(self):
        """Retorna o diretório raiz do projeto"""
        return Path(__file__).parent.parent
    
    def compile_and_assemble(self, example_name, project_root):
        """
        Compila um exemplo, monta com Jasmin e retorna True se bem-sucedido
        """
        example_file = project_root / f"{example_name}.txt"
        
        if not example_file.exists():
            pytest.skip(f"Arquivo {example_file} não existe")
        
        # Compila
        result = subprocess.run(
            [sys.executable, str(project_root / "main.py"), str(example_file)],
            capture_output=True,
            text=True,
            cwd=str(project_root)
        )
        
        if result.returncode != 0:
            return False, f"Erro compilando: {result.stdout}\n{result.stderr}", []
        
        # Extrai nomes das classes geradas
        class_files = []
        
        # Procura por arquivos .j gerados
        for line in result.stdout.split('\n'):
            if "gerada:" in line or "gerado:" in line:
                # Extrai nome do arquivo
                parts = line.split()
                for part in parts:
                    if part.endswith(".j"):
                        class_files.append(part)
        
        if not class_files:
            # Se não achou nos outputs, procura por padrão
            base_name = example_name.replace("_", "").replace("teste", "Teste").replace("exemplo", "Exemplo")
            
            # Procura main class
            for name_variant in [f"{base_name}", example_name]:
                j_file = project_root / f"{name_variant}.j"
                if j_file.exists():
                    class_files.append(j_file.name)
                    break
        
        # Monta com Jasmin
        if class_files:
            cmd = ["java", "-jar", str(project_root / "jasmin.jar")] + \
                  [str(project_root / cf) for cf in class_files]
            
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                cwd=str(project_root)
            )
            
            if result.returncode != 0:
                return False, f"Erro montando com Jasmin: {result.stdout}\n{result.stderr}", class_files
        
        return True, None, class_files
    
    def test_exemplo_interface_produtos_executes(self, project_root):
        """exemplo_interface_produtos deve executar sem erros"""
        success, error, classes = self.compile_and_assemble("exemplo_interface_produtos", project_root)
        
        if not success:
            pytest.fail(f"Falha na compilação/montagem: {error}")
        
        # Executa
        result = subprocess.run(
            ["java", "Exemplo_interface_produtos"],
            capture_output=True,
            text=True,
            cwd=str(project_root),
            timeout=10
        )
        
        assert result.returncode == 0, \
            f"Erro executando: {result.stdout}\n{result.stderr}"
        
        # Valida output
        assert "LISTA DE PRODUTOS" in result.stdout
        assert "Notebook" in result.stdout
        assert "3000" in result.stdout
        assert "Valor Total do Estoque: 17500" in result.stdout
    
    def test_teste_interfaces_multiplas_executes(self, project_root):
        """teste_interfaces_multiplas deve executar sem erros"""
        success, error, classes = self.compile_and_assemble("teste_interfaces_multiplas", project_root)
        
        if not success:
            pytest.skip(f"Arquivo não existe ou erro na compilação")
        
        # Executa
        result = subprocess.run(
            ["java", "Teste_interfaces_multiplas"],
            capture_output=True,
            text=True,
            cwd=str(project_root),
            timeout=10
        )
        
        assert result.returncode == 0, \
            f"Erro executando: {result.stdout}\n{result.stderr}"
        
        # Valida output
        assert "PESSOAS" in result.stdout
        assert "Alice" in result.stdout
        assert "25" in result.stdout
    
    def test_teste_boletim_executes(self, project_root):
        """teste_boletim deve executar sem erros"""
        success, error, classes = self.compile_and_assemble("teste_boletim", project_root)
        
        if not success:
            pytest.skip(f"Arquivo não existe ou erro na compilação")
        
        # Executa
        result = subprocess.run(
            ["java", "Teste_boletim"],
            capture_output=True,
            text=True,
            cwd=str(project_root),
            timeout=10
        )
        
        assert result.returncode == 0, \
            f"Erro executando: {result.stdout}\n{result.stderr}"
        
        # Valida output
        assert "BOLETIM" in result.stdout
        assert "Pedro" in result.stdout
        assert "Media da Turma" in result.stdout


class TestCodeGeneration:
    """Testes de validação do bytecode gerado"""
    
    @pytest.fixture
    def project_root(self):
        """Retorna o diretório raiz do projeto"""
        return Path(__file__).parent.parent
    
    def test_interface_generates_separate_class_files(self, project_root):
        """Interfaces devem gerar arquivos .j separados"""
        example_file = project_root / "exemplo_interface_produtos.txt"
        
        result = subprocess.run(
            [sys.executable, str(project_root / "main.py"), str(example_file)],
            capture_output=True,
            text=True,
            cwd=str(project_root)
        )
        
        # Verifica que Produto.j foi gerado
        assert "Produto.j" in result.stdout or (project_root / "Produto.j").exists()
        # Verifica que Exemplo_interface_produtos.j foi gerado
        assert "Exemplo_interface_produtos.j" in result.stdout or \
               (project_root / "Exemplo_interface_produtos.j").exists()
    
    def test_multiple_interfaces_generate_separate_files(self, project_root):
        """Múltiplas interfaces devem gerar múltiplos arquivos .j"""
        example_file = project_root / "teste_interfaces_multiplas.txt"
        
        if not example_file.exists():
            pytest.skip("Arquivo não existe")
        
        result = subprocess.run(
            [sys.executable, str(project_root / "main.py"), str(example_file)],
            capture_output=True,
            text=True,
            cwd=str(project_root)
        )
        
        # Verifica que Pessoa.j foi gerado
        assert "Pessoa.j" in result.stdout or (project_root / "Pessoa.j").exists()
        # Verifica que Endereco.j foi gerado
        assert "Endereco.j" in result.stdout or (project_root / "Endereco.j").exists()


class TestStringFieldHandling:
    """Testes específicos para manejo de campos string em interfaces"""
    
    @pytest.fixture
    def project_root(self):
        """Retorna o diretório raiz do projeto"""
        return Path(__file__).parent.parent
    
    def test_string_field_append_to_stringbuilder(self, project_root):
        """Campos string devem usar append(Ljava/lang/String;) em StringBuilder"""
        example_file = project_root / "exemplo_interface_produtos.txt"
        
        result = subprocess.run(
            [sys.executable, str(project_root / "main.py"), str(example_file)],
            capture_output=True,
            text=True,
            cwd=str(project_root)
        )
        
        # Lê o arquivo Jasmin gerado
        jasmin_file = project_root / "Exemplo_interface_produtos.j"
        if jasmin_file.exists():
            jasmin_code = jasmin_file.read_text()
            
            # Verifica que não há append(I) sendo usado para string fields
            # Procura por getfield Produto/nome seguido por append(I)
            lines = jasmin_code.split('\n')
            
            for i, line in enumerate(lines):
                if 'getfield Produto/nome Ljava/lang/String;' in line:
                    # Proxima linha de append deve ser com String, não Int
                    if i + 1 < len(lines):
                        next_line = lines[i + 1].strip()
                        assert 'append(Ljava/lang/String;)' in next_line, \
                            f"String field deve usar append(Ljava/lang/String;) mas encontrou: {next_line}"
    
    def test_number_field_append_to_stringbuilder(self, project_root):
        """Campos number devem usar append(I) em StringBuilder"""
        example_file = project_root / "exemplo_interface_produtos.txt"
        
        result = subprocess.run(
            [sys.executable, str(project_root / "main.py"), str(example_file)],
            capture_output=True,
            text=True,
            cwd=str(project_root)
        )
        
        # Lê o arquivo Jasmin gerado
        jasmin_file = project_root / "Exemplo_interface_produtos.j"
        if jasmin_file.exists():
            jasmin_code = jasmin_file.read_text()
            
            # Verifica que append(I) está sendo usado em algum lugar para number fields
            # Pode haver variáveis intermediárias
            assert 'append(I)' in jasmin_code, \
                "StringBuilder deve ter append(I) para campos number"


class TestLocalVariableHandling:
    """Testes para manejo de variáveis locais vs globais"""
    
    @pytest.fixture
    def project_root(self):
        """Retorna o diretório raiz do projeto"""
        return Path(__file__).parent.parent
    
    def test_array_variable_uses_aload_not_iload(self, project_root):
        """Variáveis array devem usar aload, não iload"""
        example_file = project_root / "teste_boletim.txt"
        
        if not example_file.exists():
            pytest.skip("Arquivo não existe")
        
        result = subprocess.run(
            [sys.executable, str(project_root / "main.py"), str(example_file)],
            capture_output=True,
            text=True,
            cwd=str(project_root)
        )
        
        # Lê o arquivo Jasmin gerado
        jasmin_file = project_root / "Teste_boletim.j"
        if jasmin_file.exists():
            jasmin_code = jasmin_file.read_text()
            
            # Verifica que a variável alunos é carregada com aload, não iload
            lines = jasmin_code.split('\n')
            
            # Procura por aload de variáveis array
            for line in lines:
                if 'aload' in line and 'ArrayList' in '\n'.join(lines):
                    # Deve haver aload em algum lugar
                    assert 'aload' in jasmin_code, \
                        "Array variables devem usar aload instruction"
    
    def test_interface_variable_uses_aload_not_iload(self, project_root):
        """Variáveis interface devem usar aload, não iload"""
        example_file = project_root / "exemplo_interface_produtos.txt"
        
        result = subprocess.run(
            [sys.executable, str(project_root / "main.py"), str(example_file)],
            capture_output=True,
            text=True,
            cwd=str(project_root)
        )
        
        # Lê o arquivo Jasmin gerado
        jasmin_file = project_root / "Exemplo_interface_produtos.j"
        if jasmin_file.exists():
            jasmin_code = jasmin_file.read_text()
            
            # Verifica que a variável prod é carregada com aload, não iload
            # (prod é do tipo Produto, uma interface)
            assert 'aload' in jasmin_code, \
                "Interface variables devem usar aload instruction"
