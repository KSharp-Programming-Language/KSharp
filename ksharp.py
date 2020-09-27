import ply.lex as lex
import ply.yacc as yacc

tokens = (
    'NAME','NUMBER',
    'PLUS','MINUS','TIMES','DIVIDE','EQUALS',
    'LPAREN','RPAREN',
    )

# Basic Tokens

t_PLUS    = r'\+'
t_MINUS   = r'-'
t_TIMES   = r'\*'
t_DIVIDE  = r'/'
t_EQUALS  = r'='
t_LPAREN  = r'\('
t_RPAREN  = r'\)'
t_NAME = r'[a-zA-Z_]\w*'

# Custom K# Tokens

t_AGENCY = r'^agency\b\s\b\w+\b\w*{'
t_HIATUS = r'hiatus.*' # need to think about delimited comments - how will we delimited these? like /* only the stuff inside is a comment */ for a delimited comment in many languages
t_ULTBIAS = r'^ult bias\s{1}\w+\s{1}\w+\s{1}=\s{1}.+\s{1}saranghae$'  # right now the first `\w+` is being used to represent the type of the var - we need to check to make sure it's a valid type
t_IDOL = r'^idol\s{1}\w+\s{1}\w+\s{1}(=\s{1}.+\s{1})?saranghae$' # right now the first `\w+` is being used to represent the type of the var - we need to check to make sure it's a valid type
t_TYPE = r'(fanmail|gender|ranking)'  # prototype for type, not final at all
t_NEWINSTANCE = r'^ult bias\s{1}(?P<class_name>(classname1|classname2|classname3))\s{1}\w+\s{1}=\s{1}startup\s{1}(?P=class_name)\s{1}.+\s{1}saranghae$' # classnameN list needed as a var

def t_NUMBER(t):
    r'\d+'
    try:
        t.value = int(t.value)
    except ValueError:
        print("Integer value too large %d", t.value)
        t.value = 0
    return t

# Ignored characters
t_ignore = " \t"

def t_newline(t):
    r'\n+'
    t.lexer.lineno += t.value.count("\n")
    
def t_error(t):
    print("Illegal character '%s'" % t.value[0])
    t.lexer.skip(1)
    
lexer = lex.lex()

# Parsing rules

precedence = (
    ('left','PLUS','MINUS'),
    ('left','TIMES','DIVIDE'),
    ('right','UMINUS'),
)

# dictionary of names
names = { }

def p_statement_assign(t):
    'statement : NAME EQUALS expression'
    names[t[1]] = t[3]

def p_statement_expr(t):
    'statement : expression'
    print(t[1])

def p_expression_binop(t):
    '''expression : expression PLUS expression
                  | expression MINUS expression
                  | expression TIMES expression
                  | expression DIVIDE expression'''
    if t[2] == '+'  : t[0] = t[1] + t[3]
    elif t[2] == '-': t[0] = t[1] - t[3]
    elif t[2] == '*': t[0] = t[1] * t[3]
    elif t[2] == '/': t[0] = t[1] / t[3]

def p_expression_uminus(t):
    'expression : MINUS expression %prec UMINUS'
    t[0] = -t[2]

def p_expression_group(t):
    'expression : LPAREN expression RPAREN'
    t[0] = t[2]

def p_expression_number(t):
    'expression : NUMBER'
    t[0] = t[1]

def p_expression_name(t):
    'expression : NAME'
    try:
        t[0] = names[t[1]]
    except LookupError:
        print("Undefined name '%s'" % t[1])
        t[0] = 0

def p_error(t):
    print("Syntax error at '%s'" % t.value)
parser = yacc.yacc()

while True:
    try:
        s = input('calc > ')   # Use raw_input on Python 2
    except EOFError:
        break
    parser.parse(s)