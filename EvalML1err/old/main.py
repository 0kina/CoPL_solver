import sys

from lark.lark import Lark
from lark.lexer import Token
from lark.tree import Tree

from helper import pretty
from helper import get_int, int_to_tree, make_is_form, make_evalto_form
# from eval_ml1_err import DerivateEvalNatExp
# from eval_ml1_err import derivate_is_tree

if __name__ == '__main__':
    parser = Lark.open("eval_ml1_err.lark", rel_to=__file__, lexer='basic')
    tree = parser.parse(input())
    print(tree)
    print(tree.pretty(), file=sys.stderr)
    # t2 = make_is_form("1", "lt", "2")
    t2 = make_evalto_form(int_to_tree("1"), "1")
    print(tree == t2)
    print(t2)
    print(t2.pretty(), file=sys.stderr)

    # words = []
    # DerivateEvalNatExp(words).visit(tree)

    # answer = []
    # derivate_is_tree(tree, answer)

    # print(pretty(answer))
    # TODO bool_to_treeをしっかり実装する or 削除する