import expr
from token import Token
from token_type import TokenType

class AstPrinter(expr.Interface):
    def print(self, expr):
        return expr.accept(self)

    def visitBinaryExpr(self, expr):
        return self.parenthesize(expr.operator.lexeme, expr.left, expr.right)
    
    def visitGroupingExpr(self, expr):
        return self.parenthesize("group", expr.expression)
    
    def visitLiteralExpr(self, expr):
        if expr.value == None:
            return 'nil'
        return str(expr.value)
    
    def visitUnaryExpr(self, expr):
        return self.parenthesize(expr.operator.lexeme, expr.right)

    def parenthesize(self, name, *exprs):
        string = f'({name}'
        for expr in exprs:
            string += ' '
            string += expr.accept(self)
        string += ')'
        return string

if __name__ == '__main__':
    expression = expr.Binary(
        expr.Unary(
            Token(TokenType.MINUS, "-", None, 1),
            expr.Literal(123)),
        Token(TokenType.STAR, "*", None, 1),
        expr.Grouping(
            expr.Literal(45.67)))
    print(AstPrinter().print(expression))