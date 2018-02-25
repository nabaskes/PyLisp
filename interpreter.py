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
        if symbol == 'quote':
            return left
        if symbol == 'car':
            return left.left
        if symbol == 'cdr':
            return left.right
        if symbol == 'cons':
            return self.cons(left, right)

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

    def cons(self, left, right):
        '''Not fully implemented, obviously'''
        if self.is_tree(right):
            if(self.is_tree(left)):
                pass
            return SyntaxTree('(cons '+str(left)+' '+right.raw_expr+")",
                              interpreter = self.interpreter,
                              left=left,
                              right=right)
        if self.is_tree(left):
            pass
        return SyntaxTree('(cons '+str(left)+' ' str(right)+")",
                          self.interpreter)
