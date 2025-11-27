"""
Utilitários de teste do compilador - funções auxiliares para executar o compilador TypeScript.
"""

import subprocess
import sys
from pathlib import Path


def compile_code(code: str) -> tuple:
    """
    Compila um trecho de código TypeScript.
    
    Args:
        code: código fonte TypeScript em string
    
    Returns:
        tupla (success: bool, errors: list)
        - success: True se a compilação foi bem-sucedida (sem erros)
        - errors: lista de mensagens de erro, se houver
    """
    # Write code to temporary file
    test_file = Path("/tmp/test_code.ts")
    test_file.write_text(code)
    
    try:
        # Execute compiler
        project_root = Path(__file__).parent.parent
        result = subprocess.run(
            [sys.executable, str(project_root / "main.py"), str(test_file)],
            capture_output=True,
            text=True,
            cwd=str(project_root)
        )
        
        # Parse errors from output
        errors = _extract_errors(result.stdout, result.stderr)
        
        # Success = exit code 0 and no "ERRORS FOUND" marker
        success = result.returncode == 0 and "❌ ERRORS FOUND:" not in result.stdout
        
        return (success, errors)
        
    finally:
        # Cleanup
        test_file.unlink(missing_ok=True)


def _extract_errors(stdout: str, stderr: str) -> list:
    """Extrai mensagens de erro da saída do compilador"""
    errors = []
    
    # Verifica a seção de erros no stdout (Português: ERROS ENCONTRADOS)
    if "❌ ERROS ENCONTRADOS:" in stdout:
        lines = stdout.split('\n')
        in_errors = False
        
        for line in lines:
            # Início da seção de erros
            if "❌ ERROS ENCONTRADOS:" in line:
                in_errors = True
                continue
            
            # Linha de erro (começa com hífen)
            if in_errors and line.strip().startswith("-"):
                errors.append(line.strip()[1:].strip())
            
            # Fim da seção de erros
            if in_errors and ("⚠" in line or "✔" in line):
                break
    
    # Adiciona stderr se presente
    if stderr.strip():
        errors.extend([e.strip() for e in stderr.strip().split('\n')])
    
    return errors
