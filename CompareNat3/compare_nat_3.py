from lark import Transformer, Tree, v_args
from lark.visitors import Interpreter

@v_args(inline=True)
class EvalCompareNat1(Transformer):
    def zero(self): return 0

    def succ(self, n): return n + 1

@v_args(tree=True)
class DerivateCompareNat3(Interpreter):
    def __init__(self, words):
        super().__init__()
        self.words = words

    def lt_form(self, lt_form_tree):
        l_operand, op, r_operand =lt_form_tree.children

        # L-Succ
        if l_operand == r_operand.children[0]:
            self.words.append(f"{lt_form_tree.to_string()} by L-Succ {{}}")
        # L-SuccR
        else:
            self.words.append(f"{lt_form_tree.to_string()} by L-SuccR {{")

            lt_form_tree.children = []
            lt_form_tree.children.append(
                Tree("lt_form", [
                    l_operand,
                    op,
                    r_operand.children[0]
                ])
            )

            self.visit(lt_form_tree.children[0])
            self.words.append(f"}}")