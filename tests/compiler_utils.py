import subprocess
import sys
from pathlib import Path
import re

def compile_code(code: str) -> tuple:
    """
    Compila código TypeScript usando main.py
    Retorna (success: bool, errors: list)
    """
    # Criar arquivo temporário
    test_file = Path("/tmp/test_code.ts")
    test_file.write_text(code)
    
    # Executar compilador
    project_root = Path(__file__).parent.parent
    result = subprocess.run(
        [sys.executable, str(project_root / "main.py"), str(test_file)],
        capture_output=True,
        text=True,
        cwd=str(project_root)
    )
    
    # Limpar
    test_file.unlink()
    
    # Parse de erros - podem estar em stdout ou stderr
    errors = []
    
    # Procura por "❌ ERROS ENCONTRADOS:" no stdout
    if "❌ ERROS ENCONTRADOS:" in result.stdout:
        # Extrai linhas de erro (começam com " -")
        lines = result.stdout.split('\n')
        in_errors = False
        for line in lines:
            if "❌ ERROS ENCONTRADOS:" in line:
                in_errors = True
                continue
            if in_errors and line.strip().startswith("-"):
                # Remove o " - " do início
                error_msg = line.strip()[2:]
                errors.append(error_msg)
            elif in_errors and ("⚠" in line or "✔" in line):
                break
    
    # Se houver stderr também, adiciona
    if result.stderr:
        stderr_errors = result.stderr.strip().split('\n')
        errors.extend(stderr_errors)
    
    # Sucesso se:
    # 1. Exit code é 0 E não há "❌ ERROS"
    # 2. Ou "✔ Semântica concluída sem erros" em stdout
    success = result.returncode == 0 and "❌ ERROS ENCONTRADOS:" not in result.stdout
    
    return (success, errors)
