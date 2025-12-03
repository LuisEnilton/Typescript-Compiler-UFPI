"""
TypeScript Compiler Entry Point
Simple pipeline: Lexical Analysis → Parsing → Semantic Analysis
"""
"""
Entrada do compilador estilo TypeScript
Pipeline simples: Análise Lexical → Parsing → Análise Semântica
"""

import re
import os
from TypeScriptJasminGenerate import JasminGenerator
from TypeScriptSemantic import SemanticAnalyzer
from TypeScriptParser import TypeScriptParser
from TypeScriptLexer import TypeScriptLexer
import sys
from antlr4 import FileStream, CommonTokenStream


def _derive_class_name(filepath: str) -> str:
    base = os.path.splitext(os.path.basename(filepath))[0]
    # Remove caracteres não alfanuméricos
    base = re.sub(r'[^a-zA-Z0-9_]', '_', base)
    if not base:
        base = "Output"
    # Garantir que começa com letra maiúscula para convenção Java
    if not base[0].isalpha():
        base = "C" + base
    return base[0].upper() + base[1:]


def compile_file(filepath: str) -> bool:
    """Compila um arquivo estilo TypeScript.
    Retorna True se bem-sucedido, False se erros encontrados.
    """
    print(f"Compiling: {filepath}")

    try:
        # Parse source file
        input_stream = FileStream(filepath, encoding="utf-8")
        lexer = TypeScriptLexer(input_stream)
        tokens = CommonTokenStream(lexer)
        parser = TypeScriptParser(tokens)
        tree = parser.program()

        # Semantic analysis
        analyzer = SemanticAnalyzer()
        errors = analyzer.analyze(tree)

        # Report results
        if errors:
            print("\n❌ ERROS ENCONTRADOS:\n")
            for error in errors:
                print(f"  - {error}")
            print("\n⚠ Execução abortada devido a erros semânticos.\n")
            return False

        print("✔ Semântica concluída sem erros.")

        # Jasmin (código intermediário)
        class_name = _derive_class_name(filepath)
        generator = JasminGenerator(analyzer, class_name=class_name)
        generator.visit(tree)
        jasmin_code = generator.get_result()
        jasmin_path = os.path.join(
            os.path.dirname(filepath), f"{class_name}.j")
        with open(jasmin_path, "w", encoding="utf-8") as f:
            f.write(jasmin_code)
        print(f"✔ Arquivo Jasmin gerado: {jasmin_path}")
        print("Para montar e executar:")
        print(f"  java -jar jasmin.jar {class_name}.j")
        print(f"  java {class_name}\n")
        return True

    except Exception as e:
        print(f"\n❌ COMPILATION ERROR: {e}\n")
        return False


def main():
    if len(sys.argv) != 2:
        print("USAGE:")
        print("  python main.py <file.ts>")
        print("\nExample:")
        print("  python main.py program.ts")
        sys.exit(1)

    success = compile_file(sys.argv[1])
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
