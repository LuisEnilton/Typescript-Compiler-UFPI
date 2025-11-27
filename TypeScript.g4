/**
 * Gramática estilo TypeScript (Simplificada)
 * Análise Lexical -> Parsing -> Análise Semântica
 */

grammar TypeScript;

// ============================================================================
// ESTRUTURA DO PROGRAMA
// ============================================================================

program: statement* EOF;

statement
    : variableDecl | functionDecl | interfaceDecl
    | ifStmt | whileStmt | forStmt
    | expressionStmt | returnStmt | block
    ;

block: '{' statement* '}';

// ============================================================================
// DECLARAÇÕES
// ============================================================================

variableDecl: (LET | CONST) ID ':' typeExpr (ASSIGN expression)? ';';
functionDecl: FUNCTION ID '(' paramList? ')' ':' typeExpr block;
paramList: param (',' param)*;
param: ID ':' typeExpr;
returnStmt: RETURN expression? ';';

// ============================================================================
// CONTROLE DE FLUXO
// ============================================================================

ifStmt: IF '(' expression ')' statement (ELSE statement)?;
whileStmt: WHILE '(' expression ')' statement;
forStmt: FOR '(' (variableDecl | expressionStmt | ';') expression? ';' expression? ')' statement;
expressionStmt: expression ';';

// ============================================================================
// EXPRESSÕES (Ordem de Precedência)
// ============================================================================

expression: assignmentExpr;
assignmentExpr: postfixExpr ASSIGN assignmentExpr | logicalOrExpr;
logicalOrExpr: logicalAndExpr (OR logicalAndExpr)*;
logicalAndExpr: equalityExpr (AND equalityExpr)*;
equalityExpr: relationalExpr ((EQ | NEQ) relationalExpr)*;
relationalExpr: additiveExpr ((LT | LTE | GT | GTE) additiveExpr)*;
additiveExpr: multiplicativeExpr ((PLUS | MINUS) multiplicativeExpr)*;
multiplicativeExpr: unaryExpr ((MULT | DIV | MOD) unaryExpr)*;
unaryExpr: NOT unaryExpr | postfixExpr;
postfixExpr: primary (postfixOp)*;
postfixOp: '[' expression ']' | '.' ID | '(' (expression (',' expression)*)? ')';

// ============================================================================
// EXPRESSÕES PRIMÁRIAS
// ============================================================================

primary
    : literal
    | ID
    | '(' expression ')'
    | arrayLiteral
    | objectLiteral
    ;

arrayLiteral: '[' (expression (',' expression)*)? ']';
objectLiteral: '{' (propAssign (',' propAssign)*)? '}';
propAssign: (STRING | ID) ':' expression;

// ============================================================================
// TIPOS
// ============================================================================

typeExpr: baseType ('[' ']')?;
baseType: NUMBER_TYPE | STRING_TYPE | BOOLEAN_TYPE | ID;

// ============================================================================
// INTERFACES
// ============================================================================

interfaceDecl: INTERFACE ID '{' interfaceProp* '}';
interfaceProp: ID ':' typeExpr ';';

// ============================================================================
// LITERAIS
// ============================================================================

literal: NUMBER_LIT | STRING | BOOLEAN_LIT;

// ============================================================================
// TOKENS
// ============================================================================

// Keywords
LET: 'let';
CONST: 'const';
FUNCTION: 'function';
IF: 'if';
ELSE: 'else';
WHILE: 'while';
FOR: 'for';
INTERFACE: 'interface';
RETURN: 'return';

// Primitive Types
NUMBER_TYPE: 'number';
STRING_TYPE: 'string';
BOOLEAN_TYPE: 'boolean';

// Operators
ASSIGN: '=';
PLUS: '+';
MINUS: '-';
MULT: '*';
DIV: '/';
MOD: '%';
EQ: '==';
NEQ: '!=';
LT: '<';
LTE: '<=';
GT: '>';
GTE: '>=';
AND: '&&';
OR: '||';
NOT: '!';

// Literals and Identifiers
NUMBER_LIT: [0-9]+ ('.' [0-9]+)?;
STRING: '"' (~["\\] | '\\' .)* '"' | '\'' (~['\\] | '\\' .)* '\'';
BOOLEAN_LIT: 'true' | 'false';
ID: [a-zA-Z_] [a-zA-Z0-9_]*;

// Skip whitespace and comments
WS: [ \t\r\n]+ -> skip;
LINE_COMMENT: '//' ~[\r\n]* -> skip;
BLOCK_COMMENT: '/*' .*? '*/' -> skip;
