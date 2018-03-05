from tree import SyntaxTree, split_expr, is_in


class Interpreter:
    def __init__(self):
        self.builtin = ['+', '-', '/', '*']
        self.base_functions = ['eq?', 'quote', 'cons', 'car', 'cdr', 'atom?', 'define', 'lambda', 'cond', 'eval', 'map', 'filter', 'reduce']
        self.defined = {}
        self.fake_tree = SyntaxTree('(+ 1 2)', self)

    def __call__(self, expr):
        'Evaluates a lisp expression'
        tree = SyntaxTree(expr)
        return tree()

    def evalbuiltin(self, symbol, left, right):
        if symbol == '+':
            return float(left) + float(right)
        elif symbol == '-':
            return float(left) - float(right)
        elif symbol == '/':
            return float(left)/float(right)
        elif symbol == '*':
            return float(left)*float(right)

    def eval(self, symbol, left, right):
        if symbol in self.builtin:
            return self.evalbuiltin(symbol, left, right)
        elif symbol in self.base_functions:
            return self.evalbase(symbol, left, right)
        elif symbol in self.defined.keys():
            return self.eval_lambda(self.defined[symbol], self.left)

    def evalbase(self, symbol, left, right):
        if symbol == 'eq?':
            return self.equals(left, right)
        if symbol == 'quote':
            if isinstance(left, SyntaxTree):
                return left.raw_expr
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
        if symbol == 'eval':
            return self.eval_lambda(left, right)
        if symbol == 'define':
            return self.define(left, right)
        if symbol == 'map':
            result = []
            for item in split_expr(right):
                result.append(self.eval_lamba(self.eval(split_expr(left)), result))
            return "("+" ".join(result)+")"
        if symbol == "filter":
            result = []
            for item in split_expr(right):
                if self.eval_lamba(item, left):
                    result.append(item)
            return "("+" ".join(result)+")"
        if symbol == "reduce":
            # in this version "reduce" is a foldl
            args = split_expr(right)
            res = args[0]
            for i in range(1, len(args)):
                res = self.eval_lambda("("+str(res)+" "+args[i]+")", left)
            return res

    def equals(self, left, right):
        if self.is_tree(left):
            left = left()
        if self.is_tree(right):
            right = right()
        try:
            left = float(left)
        except Exception:
            pass
        try:
            right = float(right)
        except Exception:
            pass
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
                          self)

    def def_lambda(self, args, expr):
        args = split_expr(args)
        if not isinstance(args, list):
            args = [args]
        for arg in args:
            expr = expr.raw_expr.replace(f" {arg} ", " {"+str(arg)+"} ")
        return "("+expr+" "+lisp_list(args)+")"

        # for count, arg in enumerate(tree.split_expr(expr)):
        #     expr = expr.replace(" "+arg+" ", "{a"+count+"}")
        # return expr
    # not sure this is valid, becaues you cant really programatically define variables in python

    def eval_lambda(self, lam_expr, args):
        if isinstance(lam_expr, SyntaxTree):
            lam_expr = lam_expr.raw_expr
        lam_data = split_expr(lam_expr)
        expr = lam_data[0]
        largs = split_expr(lam_data[1])
        evaluation_args = {}
        for count, arg in enumerate(largs):
            evaluation_args[arg] = args[count]
        return SyntaxTree(expr.format(**evaluation_args),
                          self)()

    def define(self, name, func):
        'Define syntax for this dialect is a bit bad.'
        '(define ((args) (actions)))'
        func_def = split_expr(func)
        args = func_def[0]
        expr = func_def[1]
        self.defined[name] = "(lambda "+self.def_lambda(args, expr)[1:]
        return


def lisp_list(data):
    return "("+' '.join(data)+")"
