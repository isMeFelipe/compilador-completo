grammar SimpAlg;

// Regras léxicas
BEGIN: 'begin';
END: 'end.';
VAR: 'var';
INT: 'int';
FLOAT: 'float';
IF: 'if';
THEN: 'then';
ELSE: 'else';
ENDIF: 'endif';
REPEAT: 'repeat';
UNTIL: 'until';
READ: 'input';
WRITE: 'print';
TRUE: 'true';
FALSE: 'false';

ASSIGN: ':=';
LPAREN: '(';
RPAREN: ')';
COLON: ':';
SEMICOLON: ';';
COMMA: ',';
DOT: '.';

ADD: '+';
SUB: '-';
MUL: '*';
DIV: '/';
MOD: '%';

GT: '>';
GE: '>=';
LT: '<';
LE: '<=';
EQ: '==';
NE: '!=';

AND: 'and';
OR: 'or';
NOT: '!';

STRING: ( '\'' ( '\\\'' | ~('\\' | '\'') )* '\''
                | '"' ( '\\' ["\\] | ~["\\] )* '"'
                );
NUMBER: DIGIT+ ('.' DIGIT+)?;
IDENTIFIER: LETTER (LETTER | DIGIT)*;

COMMENT: '{' .*? '}' -> skip;
WS: [ \t\r\n]+ -> skip;

fragment DIGIT: [0-9];
fragment LETTER: [a-zA-Z];

// Regras sintáticas
program: BEGIN statement_list END;

statement_list: statement (SEMICOLON statement)*;
statement: declaration
         | assignment
         | io_statement
         | if_statement
         | repeat_statement;

declaration: VAR variable_list COLON t_type;
variable_list: IDENTIFIER (COMMA IDENTIFIER)*;
t_type: INT | FLOAT;

assignment: IDENTIFIER ASSIGN expression;

io_statement: READ LPAREN variable_list RPAREN
            | WRITE LPAREN value_list RPAREN;
value_list: value (COMMA value)*;
value: expression | STRING | TRUE | FALSE;

if_statement: IF LPAREN boolean_expression RPAREN THEN statement_list (ELSE statement_list)? ENDIF;

repeat_statement: REPEAT statement_list UNTIL LPAREN boolean_expression RPAREN;

expression: term ((ADD | SUB) term)*;
term: factor ((MUL | DIV | MOD) factor)*;
factor: (ADD | SUB)? primary;
primary: NUMBER | IDENTIFIER | LPAREN expression RPAREN;

boolean_expression: boolean_term ((OR) boolean_term)*;
boolean_term: boolean_factor ((AND) boolean_factor)*;
boolean_factor: NOT? boolean_primary;
boolean_primary: expression (GT | GE | LT | LE | EQ | NE) expression
                | TRUE
                | FALSE
                | LPAREN boolean_expression RPAREN;
