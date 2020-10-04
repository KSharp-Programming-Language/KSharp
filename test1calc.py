import ply.lex as lex
import ply.yacc as yacc

tokens = (
    'TWEET',
    'FANMAIL',
    'LPAREN','RPAREN'
    )

# Basic Tokens

t_FANMAIL = r'[a-zA-Z_][a-zA-Z0-9_]*'
t_LPAREN  = r'\('
t_RPAREN  = r'\)'

# Ignored characters
t_ignore = " \t"

def t_newline(t):
    r'\n+'
    t.lexer.lineno += t.value.count("\n")
    
def t_error(t):
    print("Illegal character '%s'" % t.value[0])
    t.lexer.skip(1)
    
lexer = lex.lex()
######################################
def p_expression_tweet(p):
    'expression : FANMAIL'
    p[0] = p[1]

# Error rule for syntax errors
def p_error(p):
    print("Syntax error in input!")

# Build the parser
parser = yacc.yacc()

while True:
   try:
       s = input('ilovejiwon2020 > ')
   except EOFError:
       break
   if not s: continue
   result = parser.parse(s)
   print(result)