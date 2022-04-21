import sys

from lark import Lark

from helper import pretty
from eval_nat_exp import EvalEvalNatExp, DerivateEvalNatExp

if __name__ == '__main__':
    parser = Lark.open("eval_nat_exp.lark", rel_to=__file__, lexer='basic')
    tree = parser.parse(input())
    # print(tree.pretty(), file=sys.stderr)

    words = []
    DerivateEvalNatExp(words).visit(tree)

    print(pretty(words))