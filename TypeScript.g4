grammar TypeScript;

/* ============================================================
   PROGRAMA
   ============================================================ */

program: statement* EOF;


/* ============================================================
   STATEMENTS
   ============================================================ */

statement
    : variableDecl
    | functionDecl
    | interfaceDecl
    | ifStmt
    | whileStmt
    | forStmt
    | expressionStmt
    | returnStmt
    | block
    ;

block: '{' statement* '}';


/* ============================================================
   DECLARAÇÕES DE VARIÁVEIS E FUNÇÕES
   ============================================================ */

// let x: number = 10;
variableDecl:
      (LET | CONST) ID ':' typeExpr (ASSIGN expression)? ';'
    ;

// function soma(a: number): number { ... }
functionDecl:
      FUNCTION ID '(' paramList? ')' ':' typeExpr block
    ;

paramList: param (',' param)* ;
param: ID ':' typeExpr;

returnStmt: RETURN expression? ';';


/* ============================================================
   CONTROLE DE FLUXO
   ============================================================ */

ifStmt: IF '(' expression ')' statement (ELSE statement)? ;

whileStmt: WHILE '(' expression ')' statement ;

forStmt:
      FOR '('
        (variableDecl | expressionStmt | ';')
        expression?
        ';'
        expression?
      ')'
      statement
    ;

expressionStmt: expression ';';


/* ============================================================
   EXPRESSÕES COM PRECEDÊNCIA
   ============================================================ */

expression: assignmentExpr;

assignmentExpr
    : ID ASSIGN assignmentExpr              // x = y = z
    | arrayAccess ASSIGN assignmentExpr     // arr[i] = value
    | ID '.' ID ASSIGN assignmentExpr       // obj.prop = value
    | logicalOrExpr
    ;

logicalOrExpr:  logicalAndExpr  ( OR  logicalAndExpr )* ;
logicalAndExpr: equalityExpr    ( AND equalityExpr )* ;
equalityExpr:   relationalExpr  ( (EQ | NEQ) relationalExpr )* ;
relationalExpr: additiveExpr    ( (LT | LTE | GT | GTE) additiveExpr )* ;
additiveExpr:   multiplicativeExpr ( (PLUS | MINUS) multiplicativeExpr )* ;
multiplicativeExpr:
      unaryExpr ( (MULT | DIV | MOD) unaryExpr )*
    ;

unaryExpr
    : NOT unaryExpr
    | primary
    ;


/* ============================================================
   FORMAS PRIMÁRIAS
   ============================================================ */

primary
    : literal
    | ID
    | '(' expression ')'
    | arrayLiteral
    | objectLiteral
    | callExpr
    | arrayAccess
    ;

// f(x, y)
callExpr: ID '(' (expression (',' expression)*)? ')' ;

// v[10]
arrayAccess: ID '[' expression ']' ;

// [1,2,3]
arrayLiteral: '[' (expression (',' expression)*)? ']' ;

// { name: "Ana", age: 20 }
objectLiteral: '{' (propAssign (',' propAssign)*)? '}' ;
propAssign: (STRING | ID) ':' expression ;


/* ============================================================
   TIPOS
   ============================================================ */

// T[]
// number
// User
typeExpr: baseType ( '[' ']' )? ;

baseType:
      NUMBER_TYPE
    | STRING_TYPE
    | BOOLEAN_TYPE
    | ID               // nome de interface
    ;


/* ============================================================
   INTERFACES
   ============================================================ */

// interface User { name: string; age: number; }
interfaceDecl:
      INTERFACE ID '{' interfaceProp* '}'
    ;

interfaceProp: ID ':' typeExpr ';';


/* ============================================================
   LITERAIS
   ============================================================ */

literal:
      NUMBER_LIT
    | STRING
    | BOOLEAN_LIT
    ;


/* ============================================================
   LÉXICO (TOKENS)
   ============================================================ */

// palavras-chave
LET: 'let';
CONST: 'const';
FUNCTION: 'function';
IF: 'if';
ELSE: 'else';
WHILE: 'while';
FOR: 'for';
INTERFACE: 'interface';
RETURN: 'return';

// tipos primitivos
NUMBER_TYPE: 'number';
STRING_TYPE: 'string';
BOOLEAN_TYPE: 'boolean';

// operadores
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

// símbolos
SEMI: ';';
COMMA: ',';
COLON: ':';
LPAREN: '(';
RPAREN: ')';
LBRACE: '{';
RBRACE: '}';
LBRACK: '[';
RBRACK: ']';
DOT: '.';

// literais
NUMBER_LIT: [0-9]+ ('.' [0-9]+)? ;
STRING: '"' (~["\\] | '\\' .)* '"' | '\'' (~['\\] | '\\' .)* '\'' ;
BOOLEAN_LIT: 'true' | 'false' ;

// identificadores
ID: [a-zA-Z_] [a-zA-Z0-9_]* ;

// comentários e espaços
WS: [ \t\r\n]+ -> skip;
LINE_COMMENT: '//' ~[\r\n]* -> skip;
BLOCK_COMMENT: '/*' .*? '*/' -> skip;
