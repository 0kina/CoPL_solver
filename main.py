from lark import Lark, Transformer, Tree, v_args, Visitor
from lark.visitors import Interpreter

from helper import int_to_tree, pretty, to_string

ans = []

@v_args(inline=True)
class EvalExpression(Transformer):
    def zero(self): return 0

    def succ(self, n): return n + 1

@v_args(tree=True)
class DerivateExpression(Interpreter):
    def __init__(self, words):
        super().__init__()
        self.words = words

    def is_form(self, is_form_tree):
        l_operand, op, r_operand = is_form_tree.children[0].children
        rhs = is_form_tree.children[2]

        l_int = eval_trans(l_operand)

        # P-Zero
        if op.data == "plus_literal" and l_int == 0:
            self.words.append(f"{is_form_tree.to_string()} by P-Zero {{}}")
        # P-Succ
        elif op.data == "plus_literal" and l_int != 0:
            self.words.append(f"{is_form_tree.to_string()} by P-Succ {{")

            is_form_tree.children = []
            is_form_tree.children.append(
                Tree("is_form", [ \
                    Tree("plus_operand", [ \
                        l_operand.children[0], \
                        Tree("plus_literal", []), \
                        r_operand]), \
                    Tree("is_literal", []), \
                    rhs.children[0]]))

            for c in is_form_tree.children:
                self.visit(c)
            self.words.append(f"}}")
        # T-Zero
        elif op.data == "times_literal" and l_int == 0:
            self.words.append(f"{is_form_tree.to_string()} by T-Zero {{}}")
        # T-Succ
        elif op.data == "times_literal" and l_int != 0:
            self.words.append(f"{is_form_tree.to_string()} by T-Succ {{")

            n_1 = eval_trans(l_operand) - 1
            n_2 = eval_trans(r_operand)
            n_3 = n_1 * n_2

            is_form_tree.children = []
            is_form_tree.children.append(
                Tree("is_form", [ \
                    Tree("times_operand", [ \
                        int_to_tree(n_1), \
                        Tree("times_literal", []), \
                        r_operand]), \
                    Tree("is_literal", []), \
                    int_to_tree(n_3)]))
            is_form_tree.children.append(
                Tree("is_form", [ \
                    Tree("plus_operand", [ \
                        r_operand, \
                        Tree("plus_literal", []), \
                        int_to_tree(n_3)]), \
                    Tree("is_literal", []), \
                    rhs]))

            self.visit(is_form_tree.children[0])
            self.words[-1] += ";"
            self.visit(is_form_tree.children[1])
            self.words.append(f"}}")

if __name__ == '__main__':
    parser = Lark.open("copl.lark", rel_to=__file__, lexer='basic')
    tree = parser.parse(input())
    eval_trans = EvalExpression().transform

    words = []
    DerivateExpression(words).visit(tree)

    print(pretty(words))