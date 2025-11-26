import sys
from antlr4 import FileStream, CommonTokenStream

from TypeScriptLexer import TypeScriptLexer
from TypeScriptParser import TypeScriptParser

# Seu grande analisador completo
from TypeScriptSemantic import SemanticAnalyzer


def run_file(filepath):
    print(f"Executando: {filepath}")

    # 1. Carrega o arquivo
    input_stream = FileStream(filepath, encoding="utf-8")

    # 2. Lexer
    lexer = TypeScriptLexer(input_stream)
    tokens = CommonTokenStream(lexer)

    # 3. Parser
    parser = TypeScriptParser(tokens)
    tree = parser.program()

    # 4. Semântica
    analyzer = SemanticAnalyzer()
    errors = analyzer.analyze(tree)

    # 5. Exibe erros caso existam
    if errors:
        print("\n❌ ERROS ENCONTRADOS:\n")
        for e in errors:
            print(" -", e)
        print("\n⚠ Execução abortada devido a erros semânticos.\n")
        sys.exit(1)

    print("✔ Semântica concluída sem erros.")


def main():
    if len(sys.argv) != 2:
        print("USO CORRETO:")
        print("   python main.py arquivo.ts")
        sys.exit(1)

    filepath = sys.argv[1]
    run_file(filepath)


if __name__ == "__main__":
    main()
