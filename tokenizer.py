import re
import sys
import tokenize

INTEGER = 'INTEGER'
PLUS = 'PLUS'
MINUS = 'MINUS'
MUL = 'MUL'
DIV = 'DIV'
LPAREN = 'LPAREN'
RPAREN = 'RPAREN'
ASSIGN = 'ASSIGN'
ID = 'ID'
SEMI = 'SEMI'
EOF = 'EOF'
COLON = 'COLON'
SEMICOLON = 'SEMICOLON'

# Additional number patterns
Hexnumber = r'0[xX](?:_?[0-9a-fA-F])+'
Binnumber = r'0[bB](?:_?[01])+'
Octnumber = r'0[oO](?:_?[0-7])+'
Decnumber = r'(?:0(?:_?0)*|[1-9](?:_?[0-9])*)'
Intnumber = '(' + '|'.join([Hexnumber, Binnumber, Octnumber, Decnumber]) + ')'
Exponent = r'[eE][-+]?[0-9](?:_?[0-9])*'
Pointfloat = r'[0-9](?:_?[0-9])*\.(?:[0-9](?:_?[0-9])*)?' + '(?:' + Exponent + ')?'
Expfloat = r'[0-9](?:_?[0-9])*' + Exponent
Floatnumber = '(' + '|'.join([Pointfloat, Expfloat]) + ')'
Imagnumber = r'[0-9](?:_?[0-9])*[jJ]|(' + Floatnumber + r'[jJ])'
Number = '(' + '|'.join([Imagnumber, Floatnumber, Intnumber]) + ')'


class Tokenizers:
    # Token types
    
    # Regular expression patterns for tokenization
    token_patterns = [
        (r'\d+', INTEGER),        # Integer constant
        (r'\+', PLUS),            # Plus operator
        (r'-', MINUS),            # Minus operator
        (r'\*', MUL),             # Multiplication operator
        (r'/', DIV),              # Division operator
        (r'\(', LPAREN),          # Left parenthesis
        (r'\)', RPAREN),          # Right parenthesis
        (r':=', ASSIGN),          # Assignment operator
        (r';', SEMICOLON),        # Semicolon
        (r':', COLON),            # Colon
        (Number, 'NUMBER'),       # Number
        (r'[a-zA-Z_][a-zA-Z0-9_]*', 'ID'),  # Identifiers
        (r',', 'COMMA'),            # Handle commas
        (r'[a-zA-Z_][a-zA-Z0-9_]*\s*(?=\()', 'FUNCTION'),  # Function name followed by an opening parenthesis
        (r'!=', 'NOT_EQUAL'),            # Not equal operator

        # Add more token patterns for other symbols and characters
    ]

    def tokenize_file(file_path):
        with open(file_path, "rb") as file:
            tokens = list(tokenize.tokenize(file.readline))
        return tokens

    def tokenize_expr(expr):
        tokens = []
        expr = expr.replace(" ", "")  # Remove whitespace

        # Tokenize the expression using regular expressions
        while expr:
            matched = False
            for pattern, token_type in Tokenizers.token_patterns:
                match = re.match(pattern, expr)
                if match:
                    tokens.append((token_type, match.group()))
                    expr = expr[match.end():]
                    matched = True
                    break
            if not matched:
                raise ValueError(f"Invalid token: {expr[0]}")
        return tokens
    
    def explain_token(token):
        token_num = token[0]
        token_name = tokenize.tok_name[token.type]
        token_value = token[1]
        return token_num, token_name, token_value 


