from tree import SyntaxTree

class Interpreter:
    def __init__(self):
        self.builtin = ['+', '-', '/', '*']
        self.base_functions = ['eq?', 'quote', 'cons', 'car', 'cdr', 'atom?', 'define', 'lambda', 'cond']
        self.defined = {}
        self.fake_tree = SyntaxTree('(+ 1 2)', self)

    def __call__(self, expr):
        'Evaluates a lisp expression'
        tree = SyntaxTree(expr)
        return tree()

    def evalbuiltin(self, symbol, left, right):
        if symbol == '+':
            return left + right
        elif symbol == '-':
            return left - right
        elif symbol == '/':
            return left/right
        elif symbol == '*':
            return left*right

    def evalbase(self, symbol, left, right):
        if symbol == 'eq?':
            return self.equals(left, right)
        if symbol == ''

    def equals(self, left, right):
        if self.is_tree(left):
            if self.is_tree(right):
                return self.equals(left.left, right.left) and self.equals(left.right, right.right)
            return False
        if self.is_tree(right):
            return False
        return left == right

    def is_tree(self, item):
        'tests whether an item is a tree'
        return type(item) == type(self.fake_tree)
