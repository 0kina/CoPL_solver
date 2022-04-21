from lark import Transformer, Tree, v_args
from lark.visitors import Interpreter

from helper import int_to_tree

@v_args(inline=True)
class EvalCompareNat1(Transformer):
    def zero(self): return 0

    def succ(self, n): return n + 1

@v_args(tree=True)
class DerivateCompareNat2(Interpreter):
    def __init__(self, words):
        super().__init__()
        self.words = words

    def lt_form(self, lt_form_tree):
        l_operand, op, r_operand =lt_form_tree.children

        # L-Zero
        if l_operand.data == "zero":
            self.words.append(f"{lt_form_tree.to_string()} by L-Zero {{}}")
        # L-SuccSucc
        else:
            self.words.append(f"{lt_form_tree.to_string()} by L-SuccSucc {{")

            lt_form_tree.children = []
            lt_form_tree.children.append(
                Tree("lt_form", [
                    l_operand.children[0],
                    op,
                    r_operand.children[0]
                ])
            )

            self.visit(lt_form_tree.children[0])
            self.words.append(f"}}")