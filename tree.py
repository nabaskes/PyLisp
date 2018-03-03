class SyntaxTree:
    def __init__(self, expr, interpreter, left=None, right=None):
        self.raw_expr = expr
        self.interpreter = interpreter
        if not left:
            self.make_tree()
        else:
            self.left = left

    def __call__(self):
        if self.symbol == "quote":
            return self.eval()
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
        if len(split_expr(symlst[1])) > 1:
            self.left = SyntaxTree(symlst[1],
                                   self.interpreter)
        else:
            self.left = symlst[1]
        if len(symlst) == 3:
            if len(split_expr(symlst[2]))> 1:
                self.right = SyntaxTree(symlst[2],
                                        self.interpreter)
            else:
                self.right = symlst[2]
        else:
            self.right = ''
        self.naive_tree = True
        if is_in("(",  self.left) or is_in("(", self.right):
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
        return self.interpreter.eval(self.symbol,
                                     self.left,
                                     self.right)

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
    if "(" not in string:
        return string
    if string[0] == "(":
        string = string[1:]
    if string[-1] == ")":
        string = string[:-1]
    inds = [0]
    oparen = 0
    clparen = 0
    for count, char in enumerate(string):
        if char == ' ' and oparen == clparen:
            inds.append(count)
            clparen = 0
            oparen = 0
        elif char == "(":
            oparen += 1
        elif char == ")":
            clparen += 1
    res = []
    for i in range(1, len(inds)):
        res.append(string[inds[i-1]:inds[i]].strip())
    res.append(string[inds[-1]:].strip())
    return res


def is_in(item, container):
    'container is either a string, listlike, or SyntaxTree'
    if isinstance(container, SyntaxTree):
        return item in container.raw_expr
    return item in container
