from tree import SyntaxTree, split_expr, is_in


class Interpreter:
    def __init__(self):
        self.builtin = ['+', '-', '/', '*', '>', 'and', 'or', 'not']
        self.base_functions = ['eq?', 'quote', 'cons', 'car', 'cdr', 'atom?', 'define', 'lambda', 'cond', 'eval', 'bool', 'map', 'filter', 'reduce']
        self.defined = {}

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
        elif symbol == '>':
            return float(left)>float(right)
        elif symbol == 'and':
            return left and right
        elif symbol == 'or':
            return left or right
        elif symbol == 'not':
            return not left

    def eval(self, symbol, left, right):
        if symbol in self.builtin:
            return self.evalbuiltin(symbol, left, right)
        elif symbol in self.base_functions:
            return self.evalbase(symbol, left, right)
        elif symbol in self.defined.keys():
            print("running defined")
            try:
                left = left()
            except Exception as e:
                if "not callable" not in str(e):
                    raise
            if right:
                try:
                    right = right()
                except Exception as e:
                    if "not callable" not in str(e):
                        raise
                left = "("+str(left)+" "+str(right)+")"
            print(self.defined[symbol])
            print(left)
            return self.eval_lambda(self.defined[symbol], left)
        return symbol

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
        if symbol == 'cond':
            print(split_expr(right))
            print(left)
            if left:
                return SyntaxTree(split_expr(right)[0], self)()
            return SyntaxTree(split_expr(right)[1], self)()
        if symbol == 'bool':
            if left in ['True', 'true', 't', 'tr', '1', 'T']:
                return True
            return False
        if symbol == 'import':
            self.handle_import(left)

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
        if isinstance(args, SyntaxTree):
            args = args.raw_expr
        if isinstance(expr, SyntaxTree):
            expr = expr.raw_expr
        args = split_expr(args)
        if not isinstance(args, list):
            args = [args]
        for arg in args:
            # there are three cases for formatting of arguments
            expr = expr.replace(f" {arg} ", " {"+str(arg)+"} ")
            expr = expr.replace(f"({arg} ", "({"+str(arg)+"} ")
            expr = expr.replace(f" {arg})", " {"+str(arg)+"})")
        return "("+expr+" "+lisp_list(args)+")"

    def eval_lambda(self, lam_expr, args):
        if isinstance(lam_expr, SyntaxTree):
            lam_expr = lam_expr.raw_expr
        args = split_expr(args)
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
        self.defined[str(name)] = self.def_lambda(args, expr)
        return self.defined

    def handle_import(self, filename):
        ' this is mostly used to define a lot of statements'
        f = open(filename, 'r')
        exprs = f.read()
        for expr in exprs:
            SyntaxTree(expr.replace('\n', ''), self)()


def lisp_list(data):
    return "("+' '.join(data)+")"
