class Interpreter:
    def __init__(self):
        self.builtin = ['+', '-', '/', '*']
        self.functions = ['eq?', 'quote', 'cons', 'car', 'cdr', 'atom?', 'define', 'lambda', 'cond']

    def __call__(self, expr):
        'Evaluates a lisp expression'
        pass
