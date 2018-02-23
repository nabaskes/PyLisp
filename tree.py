class SyntaxTree:
    def __init__(self, expr, interpreter):
        self.raw_expr = expr
        self.interpreter = interpreter
        self.make_tree()

    def make_tree(self):
        naive_split = self.raw_expr.split(" ")
        self.symbol = naive_split[0].replace("(", "")
        if(len(naive_split) == 3):
            self.val1 = naive_split[1]
            self.val2 = naive_split[2]
            self.naive_tree = True
            return
        elif(len(naive_split) < 3):
            raise ValueError("Cannot have a lisp expression without 3 items")
        elif("(" not in naive_split[1]):
            self.val1 = naive_split[1]
            self.val2 = SyntaxTree(self.raw_expr[self.raw_expr[self.raw_expr.index(' ')+1:].index(' ')+1:-1])
            self.naive_tree = False
            return
        else:
            expr1startin = self.raw_expr(" ")+1
