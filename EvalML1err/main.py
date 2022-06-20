from lark.lark import Lark

from eval_ml1_err import derivate

if __name__ == '__main__':
    parser = Lark.open("eval_ml1_err.lark", rel_to=__file__, lexer='basic')
    tree = parser.parse(input())
    derivate(tree)