from TokenType import TokenType
from Token import Token

class Scanner():
    tokens = []
    start = 0
    current = 0
    line = 1

    def __init__(self, source):
        self.source = source

    def isAtEnd(self):
        return self.current >= len(self.source)

    def scanTokens(self):
        while not self.isAtEnd():
            self.start = self.current
            self._scanTokens()

        self.tokens.append(Token(TokenType.EOF, "", None, self.line))
        return self.tokens
    
    def _scanTokens(self):
        pass        