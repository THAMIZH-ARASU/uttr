from errors.illegal_character import IllegalCharError
from position import Position
from tokens import KEYWORDS, TT_ARROW, TT_AT, TT_COLON, TT_COMMA, TT_DIV, TT_EE, TT_EOF, TT_FLOAT, TT_GT, TT_GTE, TT_IDENTIFIER, TT_INT, TT_KEYWORD, TT_LANGLE, TT_LCURLY, TT_LPAREN, TT_LSQUARE, TT_LT, TT_LTE, TT_MINUS, TT_MOD, TT_MUL, TT_NE, TT_NEWLINE, TT_PLUS, TT_RANGLE, TT_RCURLY, TT_REGEX, TT_RPAREN, TT_RSQUARE, TT_STRING, Token
from constants import DIGITS, LETTERS, LETTERS_DIGITS


class Lexer:
    def __init__(self, fn, text):
        self.fn = fn
        self.text = text
        self.pos = Position(-1, 0, -1, fn, text)
        self.current_char = None
        self.advance()
    
    def advance(self):
        self.pos.advance(self.current_char)
        self.current_char = self.text[self.pos.idx] if self.pos.idx < len(self.text) else None

    def peek(self, offset=1):
        peek_idx = self.pos.idx + offset
        return self.text[peek_idx] if peek_idx < len(self.text) else None

    def peek_word(self):
        """Peek ahead and return the next word (identifier/keyword) after current position"""
        idx = self.pos.idx
        # Skip whitespace
        while idx < len(self.text) and self.text[idx] in ' \t':
            idx += 1
        # Read word
        word = ""
        while idx < len(self.text) and (self.text[idx].isalnum() or self.text[idx] == '_'):
            word += self.text[idx]
            idx += 1
        return word

    def make_tokens(self):
        tokens = []

        while self.current_char is not None:
            if self.current_char in ' \t':
                self.advance()
            elif self.current_char == '$':
                self.skip_comment()
            elif self.current_char in ';\n':
                tokens.append(Token(TT_NEWLINE, pos_start=self.pos))
                self.advance()
            elif self.current_char in DIGITS:
                tokens.append(self.make_number())
            elif self.current_char in LETTERS:
                tokens.append(self.make_identifier())
            elif self.current_char == '"':
                tokens.append(self.make_string())
            elif self.current_char == '+':
                tokens.append(Token(TT_PLUS, pos_start=self.pos))
                self.advance()
            elif self.current_char == '-':
                tokens.append(Token(TT_MINUS, pos_start=self.pos))
                self.advance()
            elif self.current_char == '*':
                tokens.append(Token(TT_MUL, pos_start=self.pos))
                self.advance()
            elif self.current_char == '/':
                tokens.append(Token(TT_DIV, pos_start=self.pos))
                self.advance()
            elif self.current_char == '%':
                tokens.append(Token(TT_MOD, pos_start=self.pos))
                self.advance()
            elif self.current_char == '(':
                tokens.append(Token(TT_LPAREN, pos_start=self.pos))
                self.advance()
            elif self.current_char == ')':
                tokens.append(Token(TT_RPAREN, pos_start=self.pos))
                self.advance()
            elif self.current_char == '[':
                tokens.append(Token(TT_LSQUARE, pos_start=self.pos))
                self.advance()
            elif self.current_char == ']':
                tokens.append(Token(TT_RSQUARE, pos_start=self.pos))
                self.advance()
            elif self.current_char == '{':
                tokens.append(Token(TT_LCURLY, pos_start=self.pos))
                self.advance()
            elif self.current_char == '}':
                tokens.append(Token(TT_RCURLY, pos_start=self.pos))
                self.advance()
            elif self.current_char == '!':
                token, error = self.make_not_equals()
                if error: return [], error
                tokens.append(token)
            elif self.current_char == '=':
                tokens.append(self.make_equals())
            elif self.current_char == '<':
                last_tok = tokens[-1] if len(tokens) > 0 else None
                tokens.append(self.make_less_than_or_langle(last_tok))
            elif self.current_char == '>':
                last_tok = tokens[-1] if len(tokens) > 0 else None
                tokens.append(self.make_greater_than_or_rangle(last_tok))
            elif self.current_char == ',':
                tokens.append(Token(TT_COMMA, pos_start=self.pos))
                self.advance()
            elif self.current_char == ':':
                tokens.append(Token(TT_COLON, pos_start=self.pos))
                self.advance()
            elif self.current_char == '@':
                tokens.append(Token(TT_AT, pos_start=self.pos))
                self.advance()
            else:
                pos_start = self.pos.copy()
                char = self.current_char
                self.advance()
                return [], IllegalCharError(pos_start, self.pos, "'" + char + "'")

        tokens.append(Token(TT_EOF, pos_start=self.pos))
        return tokens, None

    def make_number(self):
        num_str = ''
        dot_count = 0
        pos_start = self.pos.copy()

        while self.current_char is not None and self.current_char in DIGITS + '.':
            if self.current_char == '.':
                if dot_count == 1: break
                dot_count += 1
            num_str += self.current_char
            self.advance()

        if dot_count == 0:
            return Token(TT_INT, int(num_str), pos_start, self.pos)
        else:
            return Token(TT_FLOAT, float(num_str), pos_start, self.pos)

    def make_string(self):
        string = ''
        pos_start = self.pos.copy()
        escape_character = False
        self.advance()

        escape_characters = {
            'n': '\n',
            't': '\t',
            '"': '"',
            '\\': '\\'
        }

        while self.current_char is not None and (self.current_char != '"' or escape_character):
            if escape_character:
                string += escape_characters.get(self.current_char, self.current_char)
                escape_character = False
            else:
                if self.current_char == '\\':
                    escape_character = True
                else:
                    string += self.current_char
            self.advance()
        
        self.advance()
        return Token(TT_STRING, string, pos_start, self.pos)

    def make_regex(self):
        """Parse a regex literal (r"pattern" or r'pattern')"""
        pattern = ''
        pos_start = self.pos.copy()
        
        # Skip the 'r' prefix
        self.advance()
        
        if self.current_char not in ['"', "'"]:
            return None, IllegalCharError(pos_start, self.pos, "Expected '\"' or \"'\" after 'r'")
        
        quote_char = self.current_char
        self.advance()

        # Read the regex pattern (raw string, no escape processing except for the quote)
        while self.current_char is not None and self.current_char != quote_char:
            # Allow escaped quotes inside the pattern
            if self.current_char == '\\' and self.peek() == quote_char:
                pattern += '\\'
                self.advance()
                pattern += self.current_char
                self.advance()
            else:
                pattern += self.current_char
                self.advance()
        
        if self.current_char != quote_char:
            return None, IllegalCharError(pos_start, self.pos, f"Expected closing {quote_char}")
        
        self.advance()
        return Token(TT_REGEX, pattern, pos_start, self.pos), None

    def make_identifier(self):
        id_str = ''
        pos_start = self.pos.copy()

        while self.current_char is not None and self.current_char in LETTERS_DIGITS + '_':
            id_str += self.current_char
            self.advance()
        
        # Check if this is a regex literal (r"..." or r'...')
        if id_str == 'r' and self.current_char in ['"', "'"]:
            # Restore position to before 'r'
            self.pos = pos_start
            self.current_char = self.text[self.pos.idx] if self.pos.idx < len(self.text) else None
            token, error = self.make_regex()
            if error:
                return error
            return token

        # Check for multi-word keywords
        if id_str in ['as', 'make', 'each', 'repeat']:
            # Try to match multi-word keywords
            saved_pos = self.pos.copy()
            temp_str = id_str
            
            # Try up to two more words for multi-word keywords
            for _ in range(2):
                # Skip whitespace
                while self.current_char in ' \t':
                    self.advance()
                
                if self.current_char in LETTERS:
                    next_word = ''
                    while self.current_char is not None and self.current_char in LETTERS_DIGITS + '_':
                        next_word += self.current_char
                        self.advance()
                    
                    temp_str = temp_str + ' ' + next_word
                    
                    # Check if this combination is a keyword
                    if temp_str in KEYWORDS:
                        return Token(TT_KEYWORD, temp_str, pos_start, self.pos)
                else:
                    break
            
            # Not a multi-word keyword, restore position
            self.pos = saved_pos
            self.current_char = self.text[self.pos.idx] if self.pos.idx < len(self.text) else None

        tok_type = TT_KEYWORD if id_str in KEYWORDS else TT_IDENTIFIER
        return Token(tok_type, id_str, pos_start, self.pos)

    def make_not_equals(self):
        pos_start = self.pos.copy()
        self.advance()

        if self.current_char == '=':
            self.advance()
            return Token(TT_NE, pos_start=pos_start, pos_end=self.pos), None

        self.advance()
        return None, IllegalCharError(pos_start, self.pos, "'=' (after '!')")
    
    def make_equals(self):
        tok_type = TT_EE
        pos_start = self.pos.copy()
        self.advance()

        if self.current_char == '=':
            self.advance()
            return Token(tok_type, pos_start=pos_start, pos_end=self.pos)
        elif self.current_char == '>':
            self.advance()
            return Token(TT_ARROW, pos_start=pos_start, pos_end=self.pos)
        else:
            return Token(TT_IDENTIFIER, '=', pos_start=pos_start, pos_end=self.pos)

    def make_less_than_or_langle(self, last_token=None):
        pos_start = self.pos.copy()
        self.advance()

        if self.current_char == '=':
            self.advance()
            return Token(TT_LTE, pos_start=pos_start, pos_end=self.pos)
        
        # Check if this could be a tuple start
        # Look for: <>, <digit, <letter, <", <[, <{, <<, or whitespace before any of these
        next_char = self.current_char
        
        # Handle whitespace
        temp_idx = self.pos.idx
        while temp_idx < len(self.text) and self.text[temp_idx] in ' \t':
            temp_idx += 1
        
        if temp_idx < len(self.text):
            char_after_spaces = self.text[temp_idx]
        else:
            char_after_spaces = None
        
        # If immediately followed by > (empty tuple), it's LANGLE
        if next_char == '>':
            return Token(TT_LANGLE, pos_start=pos_start, pos_end=self.pos)
        
        # Check what came before to determine context
        # If preceded by identifier, ), ], }, or number, it's likely a comparison
        # If preceded by 'in', 'put', '=', '(', '[', '{', ',', or start, it's likely a tuple
        if last_token:
            # Comparison context: after identifier, number, ), ], }
            if last_token.type in [TT_IDENTIFIER, TT_INT, TT_FLOAT, TT_RPAREN, TT_RSQUARE, TT_RCURLY, TT_RANGLE]:
                return Token(TT_LT, pos_start=pos_start, pos_end=self.pos)
        
        # If followed by tuple-like content (after optional whitespace)
        if char_after_spaces in DIGITS + LETTERS + '"[{<>-' or char_after_spaces in ' \t':
            return Token(TT_LANGLE, pos_start=pos_start, pos_end=self.pos)
        
        # Otherwise, it's a less-than comparison
        return Token(TT_LT, pos_start=pos_start, pos_end=self.pos)

    def make_greater_than_or_rangle(self, last_token=None):
        pos_start = self.pos.copy()
        self.advance()

        if self.current_char == '=':
            self.advance()
            return Token(TT_GTE, pos_start=pos_start, pos_end=self.pos)
        
        # Check if we're likely closing a tuple by looking at the last token
        # RANGLE makes sense after:
        # 1. A value (number, identifier, string, rparen, rsquare, rangle) - normal tuple close
        # 2. Specific keywords that can be tuple elements (true, false)
        # 3. A comma - could be trailing comma before tuple close
        # 4. LANGLE - empty tuple <>
        # 
        # We must be careful: keywords like 'cycle', 'when', etc. are followed by GT in comparisons
        tuple_value_keywords = ['true', 'false']
        is_tuple_keyword = (last_token and last_token.type == TT_KEYWORD and 
                          last_token.value in tuple_value_keywords)
        
        if last_token and (last_token.type in [TT_INT, TT_FLOAT, TT_STRING, TT_IDENTIFIER,
                                                TT_RPAREN, TT_RSQUARE, TT_RANGLE, TT_COMMA, TT_LANGLE] 
                          or is_tuple_keyword):
            # Could be closing tuple or comparison
            # Check what comes next - if it's likely continuing an expression, it's comparison
            next_char = self.current_char
            
            # After tuple close, we typically see: comma, semicolon, newline, ), ], }, >
            # After comparison, we typically see: space+identifier/number
            
            # Special case: Empty tuple <> - always treat as RANGLE
            if last_token.type == TT_LANGLE:
                return Token(TT_RANGLE, pos_start=pos_start, pos_end=self.pos)
            
            # For after comma, it's definitely RANGLE if followed by close paren/bracket
            if last_token.type == TT_COMMA:
                if next_char in ',;\n)]}>':
                    return Token(TT_RANGLE, pos_start=pos_start, pos_end=self.pos)
            
            # If followed by punctuation (not whitespace), it's tuple close
            if next_char in ',;\n)]}>':
                return Token(TT_RANGLE, pos_start=pos_start, pos_end=self.pos)
            
            # If followed by whitespace, peek further to disambiguate
            if next_char in ' \t':
                peek_char = self.peek(1)
                # If followed by colon or close punctuation, it's tuple close
                if peek_char in ':,>;)\n':
                    return Token(TT_RANGLE, pos_start=pos_start, pos_end=self.pos)
                # If followed by letter, need to check if it's a keyword (tuple close) or identifier (comparison)
                # Common keywords after tuple close: in, show, and, or, etc.
                # For now, if followed by 'i' (likely 'in'), treat as tuple close
                elif peek_char and peek_char.isalpha():
                    # Peek more to see if it's 'in' keyword
                    peek_word = self.peek_word()
                    tuple_following_keywords = ['in', 'show', 'and', 'or', 'plus', 'minus', 'times', 'over']
                    if peek_word in tuple_following_keywords:
                        return Token(TT_RANGLE, pos_start=pos_start, pos_end=self.pos)
                    # Otherwise, assume comparison
                    return Token(TT_GT, pos_start=pos_start, pos_end=self.pos)
                # If followed by digit, it's comparison
                elif peek_char and peek_char.isdigit():
                    return Token(TT_GT, pos_start=pos_start, pos_end=self.pos)
        
        # Default to greater-than comparison
        return Token(TT_GT, pos_start=pos_start, pos_end=self.pos)

    def skip_comment(self):
        self.advance()
        
        # Check for multi-line comment
        if self.current_char == '[':
            self.advance()
            while True:
                if self.current_char is None:
                    break
                if self.current_char == ']':
                    if self.peek() == '$':
                        self.advance()
                        self.advance()
                        break
                self.advance()
        else:
            # Single line comment
            while self.current_char is not None and self.current_char != '\n':
                self.advance()