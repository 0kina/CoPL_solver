from lark import Lark

from helper import pretty
from compare_nat_1 import DerivateCompareNat1

if __name__ == '__main__':
    parser = Lark.open("compare_nat_1.lark", rel_to=__file__, lexer='basic')
    tree = parser.parse(input())

    words = []
    DerivateCompareNat1(words).visit(tree)

    print(pretty(words))