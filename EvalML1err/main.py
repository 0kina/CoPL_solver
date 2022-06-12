import sys

from lark import Lark, Tree, Token

from helper import pretty
from eval_ml1_err import DerivateEvalNatExp

if __name__ == '__main__':
    parser = Lark.open("eval_ml1_err.lark", rel_to=__file__, lexer='basic')
    tree = parser.parse(input())
    # print(tree.pretty(), file=sys.stderr)

    words = []
    DerivateEvalNatExp(words).visit(tree)

    print(pretty(words))