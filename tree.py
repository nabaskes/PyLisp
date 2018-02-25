class SyntaxTree:
    def __init__(self, expr, interpreter):
        self.raw_expr = expr
        self.interpreter = interpreter
        self.naive_tree = False
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
        self.first_sp = self.raw_expr.index(' ')
        self.symbol = self.raw_expr[1:self.first_sp]
        if(len(self.raw_expr.split(" ")) == 3):
            self.naive_tree = True
            self.left = self.raw_expr.split(" ")[1]
            self.right = self.raw_expr.split(" ")[2]
            return
        self.second_sp = self.first_sp + self.group_parens(self.raw_expr[self.first_sp])+1
        if self.second_sp-self.first_sp == 1:
            # the second item is not a list
            self.second_sp = self.raw_expr[self.first_sp+1:].index(' ')
        self.left = SyntaxTree(self.raw_expr[self.first_sp+1:self.second_sp],
                               self.interpreter)
        self.right = SyntaxTree(self.raw_expr[self.second_sp+1:-1],
                                self.interpreter)

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
