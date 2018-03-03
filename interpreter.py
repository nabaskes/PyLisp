from tree import SyntaxTree, split_expr


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
        if symbol == 'atom?':
            return len(split_expr(left)) == 1
        if symbol == 'lambda':
            return self.def_lambda(left, right)

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
        return isinstance(item, SyntaxTree)
        # return type(item) == type(self.fake_tree)

    def cons(self, left, right):
        if self.is_tree(right):
            if(self.is_tree(left)):
                items = list(left) + list(right)
                tree = self.right
                for item in reversed(items):
                    tree = self.cons(item, tree)
                return tree
            return SyntaxTree('(cons '+str(left)+' '+right.raw_expr+")",
                              self,
                              left=left,
                              right=right)
        if self.is_tree(left):
            return SyntaxTree('(cons '+left.raw_expr + ' '+ str(right)+')',
                              self,
                              self.cons(left.right, right))
        return SyntaxTree('(cons '+str(left)+' '+str(right)+")",
                          self.interpreter)

    def def_lambda(self, args, expr):
        for arg in args:
            expr = expr.replace(f" {arg} ", " \{"+str(arg)+"\}")
        return expr

        # for count, arg in enumerate(tree.split_expr(expr)):
        #     expr = expr.replace(" "+arg+" ", "{a"+count+"}")
        # return expr
    # not sure this is valid, becaues you cant really programatically define variables in python

    def eval_lambda(self, lam_expr, args):
        pass
