from tree import SyntaxTree
from interpreter import Interpreter


def run_test(expr, expected_result):
    kno = Interpreter()
    s = SyntaxTree(expr, kno)
    assert str(s()) == str(expected_result)


def test_add():
    run_test('(+ 1 1)', 2)
    run_test('(+ 1 3)', 4)
    run_test('(+ 10 1)', 11)
    run_test('(+ 2 11)', 13)
    run_test('(+ 13 17)', 30)
    run_test('(+ 1 .3)', 1.3)
    run_test('(+ 1 0)', 1)
    run_test('(+ 0 1)', 1)
    run_test('(+ 1 -1)', 0)
    run_test('(+ 1 -3)', -2)
    run_test('(+ -2.3 1)', -1.3)
    run_test('(+ -3 -2)', -5)
    run_test('(+ -2.3 -1)', -3.3)
    run_test('(+ 0 -2)', -2)


def test_multiply():
    run_test('(* 1 3)', 3)
    run_test('(* 3 4)', 12)
    run_test('(* 2 3)', 6)
    run_test('(* 1 11)', 11)
    run_test('(* 13 1)', 13)
    run_test('(* 0 1)', 0)
    run_test('(* 0 5)', 0)
    run_test('(* 0 11)', 0)
    run_test('(* 13 0)', 0)
    run_test('(* 0 0)', 0)
    run_test('(* 5 5)', 25)
    run_test('(* 11 11)', 121)
    run_test('(* 11 13)', 143)
    run_test('(* 0.0 11.0)', 0.0)
    run_test('(* .5 6)', 3)
    run_test('(* 1.0 1)', 1)
    run_test('(* 1.0 0.0)', 0)
    run_test('(* 1.0 .65)', .65)
    run_test('(* .65 1.0)', .65)
    run_test('(* .65 0)', 0)
    run_test('(* .65 0.0)', 0)


def test_divide():
    run_test('(/ 1 1)', 1)
    run_test('(/ 0 1)', 0)
    run_test('(/ 3 1)', 3)
    run_test('(/ 3 3)', 1)
    run_test('(/ 2 4)', .5)
    run_test('(/ 2 .5)', 4)
    run_test('(/ .2 2)', .1)
    run_test('(/ .2 .5)', .4)
    run_test('(/ -1 1)', -1)
    run_test('(/ 2 -1)', -2)
    run_test('(/ 2 -.5)', -4)
    run_test('(/ -2 1)', -2)
    run_test('(/ -2 -4)', .5)


def test_subtract():
    run_test('(- 2 1)', 1)
    run_test('(- 3 3)', 0)
    run_test('(- 3 0)', 3)
    run_test('(- 1 .5)', .5)
    run_test('(- 3 .5)', 2.5)
    run_test('(- 11 9)', 2)
    run_test('(- 27 12)', 15)
    run_test('(- 3 -1)', 4)
    run_test('(- -3 -3)', 0)
    run_test('(- -3 2)', -5)
    run_test('(- .65 .15)', .5)
    run_test('(- 1.15 .15)', 1)


def test_and():
    run_test('(and (bool True) (bool True))', 'True')
    run_test('(and (bool False) (bool True))', 'False')
    run_test('(and (bool True) (bool False))', 'False')
    run_test('(and (bool False) (bool False))', 'False')


def test_or():
    run_test('(or (bool True) (bool True))', 'True')
    run_test('(or (bool False) (bool True))', 'True')
    run_test('(or (bool True) (bool False))', 'True')
    run_test('(or (bool False) (bool False))', 'False')


def test_not():
    run_test('(not (bool False))', 'True')
    run_test('(not (bool True))', 'False')


def test_eq():
    run_test('(eq? 1 1)', 'True')
    run_test('(eq? 1 2)', 'False')
    run_test('(eq? 2 1)', 'False')
    run_test('(eq? 12 1)', 'False')
    run_test('(eq? 1 12)', 'False')
    run_test('(eq? 2 (+ 1 1))', 'True')
    run_test('(eq? (+ 3 5) (+ 7 1))', 'True')
    run_test('(eq? (+ 5 9) (+ 9 3))', 'True')
    run_test('(eq? (cons 1 (cons 2 3)) (cons 1 (cons 2 3)))')
    run_test('(eq? (cons (cons 1 (cons 2 3)) (cons 4 5)) (cons 1 (cons 2 (cons 3 cons( 4 5))))', 'True')


def test_quote():
    run_test('(quote 1)', '1')
    run_test('(quote (+ 1 1))', '(+ 1 1)')
    run_test('(quote foo)', 'foo')


def test_car():
    '''Test for `cons` and `car`'''
    run_test('(car (cons 1 2))', '1')
    run_test('(car (cons (cons 1 2) (cons 3 4)))', '1')
    run_test('(car (cdr (cons (cons 1 2) 3)))', '2')


def test_cdr():
    '''Test for `cons` and `cdr`'''
    run_test('(cdr (cons 1 2))', '2')
    run_test('(cdr (cons 1 (cons 2 3)))', '(cons 2 3)')
    run_test('(cdr (cons (cons 1 2) (cons 3 4)))', '(cons 2 (cons 3 4))')


def test_atom():
    run_test('(atom? 1)', 'True')
    run_test('(atom? True)', 'True')
    run_test('(atom? (+ 1 1))', 'False')
    run_test('(atom? (cons 1 (cons 2 3)))', 'False')
    run_test('(atom? (bool True))', 'False')


def test_lambda():
    '''Test for `eval` and `lambda`'''
    run_test('(eval (lambda q (+ q 1)) 1)', '2')
    run_test('(eval (lambda q (+ 1 q)) 1)', '2')
    run_test('(eval (lambda q (+ 11 q)) 1)', '12')
    run_test('(eval (lambda q (+ q 11)) 1)', '12')
    run_test('(eval (lambda q (+ q 12)) 11)', '23')
    run_test('(eval (lambda (q r) (+ q r)) (1 1))', '2')
    run_test('(eval (lambda (q r) (+ q r)) (11 1))', '12')
    run_test('(eval (lambda (q r) (+ q r)) (1 11))', '12')
    run_test('(eval (lambda (q r s) (+ q (- r s))) (1 3 2))', '2')
    run_test('(eval (lambda (numer denom) (/ numer denom)) (1 2))', '.5')
    run_test('(eval (lambda incr (+ incr 1)) 1)', '2')
    run_test('(eval (lambda incr (+ 1 incr)) 1)', '2')
    run_test('(eval (lambda incr (+ 12 incr)) 1)', '13')
    run_test('(+ 3 (eval (lambda (q r) (+ q r)) (1 1)))', '5')
    run_test('(eval (lambda q (* q q)) 4)', '16')


def test_cond():
    run_test('(cond (bool True) (2 1))', '2')
    run_test('(cond (bool False) (2 1)', '1')
    run_test('(cond (not (bool True)) (2 1))', '1')
    run_test('(cond (not (bool False)) (2 1))', '2')
    run_test('(cond (bool True) (2 (+ 3 5)))', '2')
    run_test('(cond (bool False) (2 (+ 3 5)))', '8')
    run_test('(cond (bool True) ((+ 2 3) 2))', '5')
    run_test('(cond (bool False) ((+ 2 3) 2))', '2')
    run_test('(cond (bool True) ((+ 2 3) (+ 2 5)))', '5')
    run_test('(cond (bool False) ((+ 2 3) (+ 2 5)))', '7')
    run_test('(cond (> 7 3) ((+ 7 1) (+ 3 1)))', '8')
    run_test('(cond (> 3 7) (1 2))', '2')


def test_define():
    pass
