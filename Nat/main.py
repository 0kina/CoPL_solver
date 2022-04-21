from lark import Lark

from helper import pretty
from nat import EvalNat, DerivateNat

if __name__ == '__main__':
    parser = Lark.open("nat.lark", rel_to=__file__, lexer='basic')
    tree = parser.parse(input())

    words = []
    DerivateNat(words).visit(tree)

    print(pretty(words))