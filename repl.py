from interpreter import Interpreter
from tree import SyntaxTree

kno = Interpreter()
while True:
    expr = input("PyLisp >>")
    s = SyntaxTree(expr, kno)
    print(s())
