TT_INT = 'INT'
TT_FLOAT = 'FLOAT'
TT_STRING = 'STRING'
TT_IDENTIFIER = 'IDENTIFIER'
TT_KEYWORD = 'KEYWORD'
TT_PLUS = 'PLUS'
TT_MINUS = 'MINUS'
TT_MUL = 'MUL'
TT_DIV = 'DIV'
TT_MOD = 'MOD'
TT_LPAREN = 'LPAREN'
TT_RPAREN = 'RPAREN'
TT_LSQUARE = 'LSQUARE'
TT_RSQUARE = 'RSQUARE'
TT_LCURLY = 'LCURLY'
TT_RCURLY = 'RCURLY'
TT_LANGLE = 'LANGLE'
TT_RANGLE = 'RANGLE'
TT_EE = 'EE'
TT_NE = 'NE'
TT_LT = 'LT'
TT_GT = 'GT'
TT_LTE = 'LTE'
TT_GTE = 'GTE'
TT_COMMA = 'COMMA'
TT_COLON = 'COLON'
TT_SEMICOLON = 'SEMICOLON'
TT_AT = 'AT'
TT_ARROW = 'ARROW'
TT_NEWLINE = 'NEWLINE'
TT_EOF = 'EOF'

KEYWORDS = [
    'put',
    'in',
    'keep',
    'as',
    'show',
    'when',
    'otherwise',
    'end',
    'cycle',
    'from',
    'to',
    'step',
    'each',
    'through',
    'as long as',
    'repeat while',
    'make function',
    'lambda',
    'give',
    'and',
    'or',
    'not',
    'true',
    'false',
    'cut',
    'skip',
    'attempt',
    'handle',
    'bring',
    'share',
    'check',
    'whether',
    'default',
]

class Token:
    def __init__(self, type_, value=None, pos_start=None, pos_end=None):
        self.type = type_
        self.value = value

        if pos_start:
            self.pos_start = pos_start.copy()
            self.pos_end = pos_start.copy()
            self.pos_end.advance()

        if pos_end:
            self.pos_end = pos_end.copy()

    def matches(self, type_, value):
        return self.type == type_ and self.value == value
    
    def __repr__(self):
        if self.value:
            return f'{self.type}:{self.value}'
        return f'{self.type}'