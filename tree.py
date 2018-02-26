class SyntaxTree:
    def __init__(self, expr, interpreter, left=None, right=None):
        self.raw_expr = expr
        self.interpreter = interpreter
        if not self.left:
            self.make_tree()

    def __call__(self):
        try:
            self.left = self.left()
        except Exception:
            # left is not a SyntaxTree
            pass
        try:
            self.right = self.right()
        except Exception:
            pass
        return self.eval()

    def make_tree(self):
        symlst = split_expr(self.raw_expr)
        self.symbol = symlst[0]
        self.left = SyntaxTree(symlst[1],
                               self.interpreter)
        if len(symlst) == 3:
            self.right = SyntaxTree(symlst[2],
                                    self.interpreter)
        self.naive_tree = True
        if "(" in self.left or "(" in self.right:
            self.naive_tree = False

    def group_parens(self, string):
        'returns the index of the parenthesis that corresponds to the first one in the string given'
        opens = 0
        closes = 0
        for i in range(len(string)):
            if string[i] == "(":
                opens += 1
            elif string[i] == ")":
                closes += 1
            if opens == closes:
                return i
        raise(ValueError("Open Paren doesn't have a corresponding close paren"))

    def eval(self):
        if self.symbol in self.interpreter.builtin:
            return self.interpreter.evalbuiltin(self.symbol,
                                                self.left,
                                                self.right)
        elif self.symbol in self.interpreter.base_functions:
            return self.interpreter.evalbase(self.symbol,
                                             self.left,
                                             self.right)
        elif self.symbol in self.interpreter.defined.keys():
            return self.interpreter.defined[self.symbol].format()

    def __list__(self):
        if self.symbol == 'cons':
            if self.interpreter.is_tree(self.left):
                if self.intrepeter.is_tree(self.right):
                    return list(self.left) + list(self.right)
                return list(self.left) + [self.right]
            if self.interpreter.is_tree(self.right):
                return [self.left] + list(self.right)
            return [self.left, self.right]
        return [self.raw_expr]


def split_expr(string):
    if string[0] == "(":
        string = string[1:]
    if string[-1] == ")":
        string = string[:-1]
    oparen = 0
    clparen = 0
    inds = [0]
    for i in range(len(string)):
        if string[i] == ' ' and oparen == clparen:
            inds.append(i)
            oparen = 0
            clparen = 0
        if string[i] == "(":
            oparen += 1
        if string[i] == ")":
            clparen += 1
    res = []
    for i in range(1, len(inds)):
        res.append(res[inds[i-1]:inds[i]])
    return res
