# Compilador Simplificado TypeScript (UFPI)

Este projeto implementa um compilador simplificado inspirado em TypeScript. Ele realiza:
1. Análise Léxica
2. Parsing (ANTLR4)
3. Análise Semântica (checagem de tipos, escopos, interfaces, arrays, etc.)

## Arquitetura

- **Gramática (`TypeScript.g4`)**: Define a sintaxe da linguagem (declarações, expressões, tipos, interfaces). Comentários em português explicam cada seção.
- **Arquivos Gerados (ANTLR)**: `TypeScriptLexer.py`, `TypeScriptParser.py`, `TypeScriptVisitor.py`, `TypeScriptListener.py` são gerados a partir da gramática (não editar manualmente). Se a gramática mudar, regenerar.
- **Analisador Semântico (`TypeScriptSemantic.py`)**:
  - Implementa classes de tipos (primitivos, arrays, interfaces).
  - Mantém tabela de símbolos global para variáveis, funções e interfaces.
  - Executa validações: tipos em atribuições, retorno de função, membros de interface, homogeneidade de arrays, acesso a propriedades e índices.
  - Produz mensagens de erro em português com linha e coluna.
- **Entrada do Compilador (`main.py`)**: Orquestra lexing → parsing → análise semântica. Exibe resumo: sucesso ou lista de erros.
- **Utilitários de Teste (`tests/compiler_utils.py`)**: Funções para compilar snippets durante testes.
- **Arquivos de Exemplo (`exemplo_*.txt`)**: Casos simples para testar rapidamente.
- **Testes (`pytest`)**: Conjunto validando cenários de declarações, funções, interfaces, arrays e erros semânticos.

## Dependências

Gerenciadas via Poetry (definidas em `pyproject.toml`):
- Runtime: `antlr4-python3-runtime ^4.13.2`
- Dev: `pytest ^7.4.0`
- Python: `>=3.12` (especificado `^3.12` no Poetry)

## Instalação

Pré-requisitos:
- Python 3.12 instalado
- Poetry instalado (`pip install poetry` ou conforme documentação oficial)

Passos:
```bash
# Clonar o repositório
git clone <url-do-repo>
cd CompiladorTypeUfpi

# Instalar dependências
poetry install

# Ativar shell virtual (opcional)
poetry shell
```

## Uso Básico

### Compilar um arquivo fonte (análise semântica)
```bash
poetry run python main.py exemplo_1.txt
```

### Gerar Bytecode Java

O compilador agora suporta geração de **código Jasmin** (intermediário Java) que pode ser compilado em bytecode executável.

#### 1. Compilar e Gerar Jasmin
```bash
poetry run python main.py exemplo_interface_produtos.txt
```

Isso gera:
- `Produto.j` - Classe Java para interface Produto
- `Exemplo_interface_produtos.j` - Classe principal com código compilado

#### 2. Montar Jasmin para Bytecode
```bash
java -jar jasmin.jar Produto.j Exemplo_interface_produtos.j
```

Gera:
- `Produto.class` - Bytecode da interface
- `Exemplo_interface_produtos.class` - Bytecode principal

#### 3. Executar o Código
```bash
java Exemplo_interface_produtos
```

#### Exemplo Completo
```bash
# Compilar TypeScript para Jasmin
poetry run python main.py exemplo_interface_produtos.txt

# Montar Jasmin para bytecode
java -jar jasmin.jar Produto.j Exemplo_interface_produtos.j

# Executar
java Exemplo_interface_produtos
```

### Executar todos os testes
```bash
poetry run pytest -q
```

### Executar testes de compilação e execução
```bash
poetry run pytest tests/test_examples_execution.py -v
```

## Exemplos de Código

### 1. Declaração de Variáveis e Atribuição
```typescript
let x: number = 10;
const msg: string = "Olá";
x = x + 5; // válido
msg = "mudar"; // erro: const não pode ser reatribuída
```

### 2. Função com Retorno
```typescript
function soma(a: number, b: number): number {
  return a + b;
}
let r: number = soma(2, 3);
```

### 3. Interface e Objeto (Com Geração de Bytecode)
```typescript
interface User {
  id: number;
  nome: string;
}

### 4. Arrays Homogêneos
```typescript
let nums: number[] = [1, 2, 3];
nums[0] = 5;
let pessoas: User[] = [ { id: 1, nome: "Ana" }, { id: 2, nome: "Bia" } ];
```

### 5. Erro de Tipo em Atribuição
```typescript
let x: number = 10;
let y: string = "texto";
x = y; // erro de tipo
```

### 6. Erro de Propriedade Inexistente
```typescript
interface User { id: number; nome: string; }
let u: User = { id: 1, nome: "Ana" };
let z = u.email; // erro: propriedade não definida
```

## Regenerar Gramática (se necessário)

Se `TypeScript.g4` for alterado:
```bash
# Exemplo de comando (ajuste o caminho do JAR conforme instalação)
java -jar antlr-4.13.2-complete.jar -Dlanguage=Python3 TypeScript.g4
```
Certifique-se de ter o JAR do ANTLR disponível. Depois disso, os arquivos gerados serão atualizados.

## Estrutura de Erros

Erros são reportados no formato:
```
linha:coluna - mensagem
```
Exemplo:
```
3:15 - tipo incompatível em atribuição: esperado 'number', encontrado 'string'
```

## Fluxo Interno (Resumo)
1. `main.py` lê arquivo e inicializa lexer/parser.
2. Árvore sintática é enviada ao analisador semântico.
3. Tabela de símbolos é populada (variáveis, funções, interfaces).
4. Expressões são validadas recursivamente.
5. Erros acumulados são emitidos ao final.