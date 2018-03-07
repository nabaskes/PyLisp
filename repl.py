from interpreter import Interpreter
from tree import SyntaxTree
import sys
import traceback

kno = Interpreter()
while True:
    expr = input("PyLisp >>")
    s = SyntaxTree(expr, kno)
    try:
        stdout = s()
    except Exception:
        print("PyLisp error, printing stack trace:")
        print("-"*60)
        traceback.print_exc(file=sys.stdout)
        print("-"*60)
        continue
    print(stdout)
