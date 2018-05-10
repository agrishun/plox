from .token_type import TokenType
from .token import Token

class Scanner():

    def __init__(self, source):
        self.source = source
        self.tokens = []

        self.start = 0
        self.current = 0
        self.line = 1

        self.keywords = {
            'and': TokenType.AND,
            'class': TokenType.CLASS,
            'else': TokenType.ELSE,
            'false': TokenType.FALSE,
            'for': TokenType.FOR,
            'fun': TokenType.FUN,
            'if': TokenType.IF,
            'nil': TokenType.NIL,
            'or': TokenType.OR,
            'print': TokenType.PRINT,
            'return': TokenType.RETURN,
            'super': TokenType.SUPER,
            'this': TokenType.THIS,
            'true': TokenType.TRUE,
            'var': TokenType.VAR,
            'while': TokenType.WHILE
        }

    def is_at_end(self):
        return self.current >= len(self.source)

    def add_token(self, token_type, literal=None):
        text = self.source[self.start:self.current]
        self.tokens.append(Token(token_type, text, literal, self.line))

    def scan_tokens(self):
        while not self.is_at_end():
            self.start = self.current
            self.scan_token()

        self.tokens.append(Token(TokenType.EOF, "", None, self.line))
        return self.tokens
    
    def advance(self):
        self.current += 1
        return self.source[self.current - 1]

    def match(self, expected_char):
        if self.is_at_end():
            return False
        if self.source[self.current] != expected_char:
            return False
        
        self.current += 1
        return True

    def peek(self):
        if self.is_at_end():
            return '\0'
        return self.source[self.current]

    def peek_next(self):
        if self.current + 1 >= len(self.source):
            return '\0'
        return self.source[self.current + 1]

    def string(self):
        while self.peek() != '"' and not self.is_at_end():
            if self.peek() == '\n':
                self.line += 1
            self.advance()
        if self.is_at_end():
            print(self.line, "Unterminated string.")
            return
        self.advance()
        value = self.source[self.start+1:self.current-1]
        self.add_token(TokenType.STRING, value)

    def is_digit(self, c):
        return c >= '0' and c <= '9'

    def number(self):
        while self.is_digit(self.peek()):
            self.advance()
        if self.peek() == '.' and self.is_digit(self.peek_next()):
            self.advance()
            while self.is_digit(self.peek()):
                self.advance()
        string = self.source[self.start:self.current]
        self.add_token(TokenType.NUMBER, float(string))

    def is_alpha(self, c):
        return (c >= 'a' and c <= 'z') or (c >= 'A' and c <= 'Z') or c == '_'

    def identifier(self):
        while self.is_alpha_numeric(self.peek()):
            self.advance()

        text = self.source[self.start:self.current]

        token_type = self.keywords.get(text)
        if token_type is None:
            token_type = TokenType.IDENTIFIER

        self.add_token(token_type)


    def is_alpha_numeric(self, c):
        return self.is_digit(c) or self.is_alpha(c)

    def scan_token(self):
        char = self.advance()

        if char == '(':
            self.add_token(TokenType.LEFT_PAREN)
        elif char == ')':
            self.add_token(TokenType.RIGHT_PAREN)
        elif char == '{':
            self.add_token(TokenType.LEFT_BRACE)
        elif char == '}':
            self.add_token(TokenType.RIGHT_BRACE)
        elif char == ',':
            self.add_token(TokenType.COMMA)
        elif char == '.':
            self.add_token(TokenType.DOT)
        elif char == '-':
            self.add_token(TokenType.MINUS)
        elif char == '+':
            self.add_token(TokenType.PLUS)
        elif char == ';':
            self.add_token(TokenType.SEMICOLON)
        elif char == '*':
            self.add_token(TokenType.STAR)
        elif char == '!':
            self.add_token(TokenType.BANG_EQUAL if self.match('=') else TokenType.BANG)
        elif char == '=':
            self.add_token(TokenType.EQUAL_EQUAL if self.match('=') else TokenType.EQUAL)
        elif char == '<':
            self.add_token(TokenType.LESS_EQUAL if self.match('=') else TokenType.LESS)
        elif char == '>':
            self.add_token(TokenType.GREATER_EQUAL if self.match('=') else TokenType.GREATER)
        elif char == '/':
            if self.match('/'):
                while (self.peek() != '\n' and not self.is_at_end()):
                    self.advance()
            else:
                self.add_token(TokenType.SLASH)
        elif char in  [' ', '\r', '\t']:
            pass
        elif char == '\n':
            self.line += 1
        elif char == '"':
            self.string()
        else:
            if self.is_digit(char):
                self.number()
            elif self.is_alpha(char):
                self.identifier()
            else:
                print(self.line, "Unexpected character.")