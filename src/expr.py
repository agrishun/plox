from abc import ABC, abstractmethod
class Interface(ABC):
	@abstractmethod
	def visitBinaryExpr(self, expr): raise NotImplementedError

	@abstractmethod
	def visitGroupingExpr(self, expr): raise NotImplementedError

	@abstractmethod
	def visitLiteralExpr(self, expr): raise NotImplementedError

	@abstractmethod
	def visitUnaryExpr(self, expr): raise NotImplementedError

class Binary():
	def __init__(self, left, operator, right):
		self.left = left
		self.operator = operator
		self.right = right
	def accept(self, visitor):
		return visitor.visitBinaryExpr(self)

class Grouping():
	def __init__(self, expression):
		self.expression = expression
	def accept(self, visitor):
		return visitor.visitGroupingExpr(self)

class Literal():
	def __init__(self, value):
		self.value = value
	def accept(self, visitor):
		return visitor.visitLiteralExpr(self)

class Unary():
	def __init__(self, operator, right):
		self.operator = operator
		self.right = right
	def accept(self, visitor):
		return visitor.visitUnaryExpr(self)

