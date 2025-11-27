"""
TypeScript Compiler Entry Point
Simple pipeline: Lexical Analysis → Parsing → Semantic Analysis
"""
"""
Entrada do compilador estilo TypeScript
Pipeline simples: Análise Lexical → Parsing → Análise Semântica
"""

import sys
from antlr4 import FileStream, CommonTokenStream
from TypeScriptLexer import TypeScriptLexer
from TypeScriptParser import TypeScriptParser
from TypeScriptSemantic import SemanticAnalyzer


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
        
        print("✔ Semântica concluída sem erros.\n")
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
