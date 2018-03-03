from interpreter import Interpreter
from tree import SyntaxTree

kno = Interpreter()
while True:
    expr = input("PyLisp >>")
    s = SyntaxTree(expr, kno)
    stdout = s()
    if isinstance(stdout, SyntaxTree):
        print(stdout.raw_expr)
    else:
        print(stdout)
