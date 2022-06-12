# reduce_star_exp の処理がわからなかった
import sys

from lark import Transformer, Tree, v_args
from lark.visitors import Interpreter

from helper import int_to_tree

@v_args(inline=True)
class EvalReduceNatExp(Transformer):
    def __default__(self, data, children, meta): return None

    def zero(self): return 0

    def succ(self, n): return n + 1

    def plus_exp(self, l, _, r): return l + r

    def times_exp(self, l, _, r): return l * r

    def paren_exp(self, _l, core, _r): return core

@v_args(tree=True)
class DerivateReduceNatExp(Interpreter):
    def __init__(self, words):
        super().__init__()
        self.words = words

    def is_form(self, is_form_tree):
        l_operand, op, r_operand = is_form_tree.children[0].children
        rhs = is_form_tree.children[2]

        l_int = EvalEvalNatExp().transform(l_operand)

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

            n_1 = EvalEvalNatExp().transform(l_operand) - 1
            n_2 = EvalEvalNatExp().transform(r_operand)
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

    def evalto_form(self, evalto_form_tree):
        lhs, op, rhs = evalto_form_tree.children

        # E-Const
        if lhs == rhs:
            self.words.append(f"{evalto_form_tree.to_string()} by E-Const {{}}")
        elif lhs.data == "paren_exp":
            self.visit(
                Tree("evalto_form", [lhs.children[1], op, rhs])
            )
        # E-Plus
        elif lhs.data == "plus_exp":
            self.words.append(f"{evalto_form_tree.to_string()} by E-Plus {{")

            l_operand, _, r_operand = lhs.children

            l_int = EvalEvalNatExp().transform(l_operand)
            r_int = EvalEvalNatExp().transform(r_operand)

            evalto_form_tree.children = []
            evalto_form_tree.children.extend([
                Tree("evalto_form", [
                    l_operand, op, int_to_tree(l_int)
                ]),
                Tree("evalto_form", [
                    r_operand, op, int_to_tree(r_int)
                ]),
                Tree("is_form", [
                    Tree("plus_operand", [
                        int_to_tree(l_int),
                        Tree("plus_literal", []),
                        int_to_tree(r_int),
                    ]),
                    Tree("is_literal", []),
                    rhs
                ])
            ])

            for i in range(3):
                self.visit(evalto_form_tree.children[i])

                if i < 2: self.words[-1] += ";"

            self.words.append("}")
        # E-Times
        elif lhs.data == "times_exp":
            self.words.append(f"{evalto_form_tree.to_string()} by E-Times {{")

            l_operand, _, r_operand = lhs.children
            l_int = EvalEvalNatExp().transform(l_operand)
            r_int = EvalEvalNatExp().transform(r_operand)

            evalto_form_tree.children = []
            evalto_form_tree.children.extend([
                Tree("evalto_form", [
                    l_operand, op, int_to_tree(l_int)
                ]),
                Tree("evalto_form", [
                    r_operand, op, int_to_tree(r_int)
                ]),
                Tree("is_form", [
                    Tree("times_operand", [
                        int_to_tree(l_int),
                        Tree("times_literal", []),
                        int_to_tree(r_int),
                    ]),
                    Tree("is_literal", []),
                    rhs
                ])
            ])

            for i in range(3):
                self.visit(evalto_form_tree.children[i])

                if i < 2: self.words[-1] += ";"

            self.words.append("}")

    def reduce_form(self, reduce_form_tree):
        lhs, op, rhs = reduce_form_tree.children

        print(f"op: {op}")

        # E-Const
        if op.data == "reduce_once_form":
            if rhs.data in ["zero", "succ"]:
                if lhs.data == "plus_exp":
                    self.words.append(f"{reduce_form_tree.to_string()} by R-Plus {{}}")
                else:
                    self.words.append(f"{reduce_form_tree.to_string()} by R-Times {{}}")
            elif rhs.data == "plus_exp":
                l_lhs, _, l_rhs = lhs.children
                r_lhs, _, r_rhs = rhs.children

                if l_rhs == r_rhs:
                    self.words.append(f"{reduce_form_tree.to_string()} by R-PlusL {{")

                    reduce_form_tree.children = [
                        Tree("reduce_once_form", [
                            l_lhs, op, r_lhs
                        ])
                    ]

                    self.visit(reduce_form_tree.children[0])

                    self.words.append(f"}}")
                else:
                    self.words.append(f"{reduce_form_tree.to_string()} by R-PlusR {{}}")

                    reduce_form_tree.children = [
                        Tree("reduce_once_form", [
                            l_rhs, op, r_rhs
                        ])
                    ]

                    self.visit(reduce_form_tree.children[0])

                    self.words.append(f"}}")
            else:
                l_lhs, _, l_rhs = lhs.children
                r_lhs, _, r_rhs = rhs.children

                if l_rhs == r_rhs:
                    self.words.append(f"{reduce_form_tree.to_string()} by R-TimesL {{")

                    reduce_form_tree.children = [
                        Tree("reduce_once_form", [
                            l_lhs, op, r_lhs
                        ])
                    ]

                    self.visit(reduce_form_tree.children[0])

                    self.words.append(f"}}")
                else:
                    self.words.append(f"{reduce_form_tree.to_string()} by R-TimesR {{}}")

                    reduce_form_tree.children = [
                        Tree("reduce_once_form", [
                            l_rhs, op, r_rhs
                        ])
                    ]

                    self.visit(reduce_form_tree.children[0])

                    self.words.append(f"}}")

        elif op.data == "reduce_d_form":
            if rhs.data in ["zero", "succ"]:
                if lhs.data == "plus_exp":
                    self.words.append(f"{reduce_form_tree.to_string()} by DR-Plus {{}}")
                else:
                    self.words.append(f"{reduce_form_tree.to_string()} by DR-Times {{}}")
            elif rhs.data == "plus_exp":
                l_lhs, _, l_rhs = lhs.children
                r_lhs, _, r_rhs = rhs.children

                if l_rhs == r_rhs:
                    self.words.append(f"{reduce_form_tree.to_string()} by DR-PlusL {{")

                    reduce_form_tree.children = [
                        Tree("reduce_d_form", [
                            l_lhs, op, r_lhs
                        ])
                    ]

                    self.visit(reduce_form_tree.children[0])

                    self.words.append(f"}}")
                else:
                    self.words.append(f"{reduce_form_tree.to_string()} by DR-PlusR {{}}")

                    reduce_form_tree.children = [
                        Tree("reduce_d_form", [
                            l_rhs, op, r_rhs
                        ])
                    ]

                    self.visit(reduce_form_tree.children[0])

                    self.words.append(f"}}")
            else:
                l_lhs, _, l_rhs = lhs.children
                r_lhs, _, r_rhs = rhs.children

                if l_rhs == r_rhs:
                    self.words.append(f"{reduce_form_tree.to_string()} by DR-TimesL {{")

                    reduce_form_tree.children = [
                        Tree("reduce_once_form", [
                            l_lhs, op, r_lhs
                        ])
                    ]

                    self.visit(reduce_form_tree.children[0])

                    self.words.append(f"}}")
                else:
                    self.words.append(f"{reduce_form_tree.to_string()} by DR-TimesR {{}}")

                    reduce_form_tree.children = [
                        Tree("reduce_once_form", [
                            l_rhs, op, r_rhs
                        ])
                    ]

                    self.visit(reduce_form_tree.children[0])

                    self.words.append(f"}}")

        else:
            if lhs == rhs:
                self.words.append(f"{reduce_form_tree.to_string()} by MR-Zero {{}}")

            if rhs.data in ["zero", "succ"]:
                if lhs.data == "plus_exp":
                    self.words.append(f"{reduce_form_tree.to_string()} by DR-Plus {{}}")
                else:
                    self.words.append(f"{reduce_form_tree.to_string()} by DR-Times {{}}")
            elif rhs.data == "plus_exp":
                l_lhs, _, l_rhs = lhs.children
                r_lhs, _, r_rhs = rhs.children

                if l_rhs == r_rhs:
                    self.words.append(f"{reduce_form_tree.to_string()} by DR-PlusL {{")

                    reduce_form_tree.children = [
                        Tree("reduce_d_form", [
                            l_lhs, op, r_lhs
                        ])
                    ]

                    self.visit(reduce_form_tree.children[0])

                    self.words.append(f"}}")
                else:
                    self.words.append(f"{reduce_form_tree.to_string()} by DR-PlusR {{}}")

                    reduce_form_tree.children = [
                        Tree("reduce_d_form", [
                            l_rhs, op, r_rhs
                        ])
                    ]

                    self.visit(reduce_form_tree.children[0])

                    self.words.append(f"}}")
            else:
                l_lhs, _, l_rhs = lhs.children
                r_lhs, _, r_rhs = rhs.children

                if l_rhs == r_rhs:
                    self.words.append(f"{reduce_form_tree.to_string()} by DR-TimesL {{")

                    reduce_form_tree.children = [
                        Tree("reduce_once_form", [
                            l_lhs, op, r_lhs
                        ])
                    ]

                    self.visit(reduce_form_tree.children[0])

                    self.words.append(f"}}")
                else:
                    self.words.append(f"{reduce_form_tree.to_string()} by DR-TimesR {{}}")

                    reduce_form_tree.children = [
                        Tree("reduce_once_form", [
                            l_rhs, op, r_rhs
                        ])
                    ]

                    self.visit(reduce_form_tree.children[0])

                    self.words.append(f"}}")




        if lhs.data == "paren_exp":
            self.visit(
                Tree("evalto_form", [lhs.children[1], op, rhs])
            )
        # E-Plus
        elif lhs.data == "plus_exp":
            self.words.append(f"{reduce_form_tree.to_string()} by E-Plus {{")

            l_operand, _, r_operand = lhs.children

            reduce_form_tree.children = []
            reduce_form_tree.children.extend([
                Tree("evalto_form", [
                    l_operand, op, int_to_tree(l_int)
                ]),
                Tree("evalto_form", [
                    r_operand, op, int_to_tree(r_int)
                ]),
                Tree("is_form", [
                    Tree("plus_operand", [
                        int_to_tree(l_int),
                        Tree("plus_literal", []),
                        int_to_tree(r_int),
                    ]),
                    Tree("is_literal", []),
                    rhs
                ])
            ])

            for i in range(3):
                self.visit(reduce_form_tree.children[i])

                if i < 2: self.words[-1] += ";"

            self.words.append("}")
        # E-Times
        elif lhs.data == "times_exp":
            self.words.append(f"{reduce_form_tree.to_string()} by E-Times {{")

            l_operand, _, r_operand = lhs.children
            l_int = EvalEvalNatExp().transform(l_operand)
            r_int = EvalEvalNatExp().transform(r_operand)

            reduce_form_tree.children = []
            reduce_form_tree.children.extend([
                Tree("evalto_form", [
                    l_operand, op, int_to_tree(l_int)
                ]),
                Tree("evalto_form", [
                    r_operand, op, int_to_tree(r_int)
                ]),
                Tree("is_form", [
                    Tree("times_operand", [
                        int_to_tree(l_int),
                        Tree("times_literal", []),
                        int_to_tree(r_int),
                    ]),
                    Tree("is_literal", []),
                    rhs
                ])
            ])

            for i in range(3):
                self.visit(reduce_form_tree.children[i])

                if i < 2: self.words[-1] += ";"

            self.words.append("}")