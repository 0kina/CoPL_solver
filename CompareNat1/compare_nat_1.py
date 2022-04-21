from lark import Transformer, Tree, v_args
from lark.visitors import Interpreter

from helper import int_to_tree

@v_args(inline=True)
class EvalCompareNat1(Transformer):
    def zero(self): return 0

    def succ(self, n): return n + 1

@v_args(tree=True)
class DerivateCompareNat1(Interpreter):
    def __init__(self, words):
        super().__init__()
        self.words = words

    def lt_form(self, lt_form_tree):
        l_operand, op, r_operand =lt_form_tree.children

        l_int = EvalCompareNat1().transform(l_operand)
        r_int = EvalCompareNat1().transform(r_operand)

        # L-Succ
        if l_int + 1 == r_int:
            self.words.append(f"{lt_form_tree.to_string()} by L-Succ {{}}")
        # L-Trans
        else:
            self.words.append(f"{lt_form_tree.to_string()} by L-Trans {{")

            lt_form_tree.children = []
            lt_form_tree.children.append(
                Tree("lt_form", [
                    l_operand,
                    op,
                    int_to_tree(r_int - 1)
                ])
            )
            lt_form_tree.children.append(
                Tree("lt_form", [
                    int_to_tree(r_int - 1),
                    op,
                    r_operand
                ])
            )

            self.visit(lt_form_tree.children[0])
            self.words[-1] += ";"
            self.visit(lt_form_tree.children[1])
            self.words.append(f"}}")