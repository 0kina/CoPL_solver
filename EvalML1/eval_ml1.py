import sys

from lark import Transformer, Tree, v_args
from lark.visitors import Interpreter

from helper import int_to_tree

@v_args(inline=True)
class EvalEvalML1(Transformer):
    def __default__(self, data, children, meta): raise Exception

    def zero(self): return 0

    def succ(self, n): return n + 1

    def int(self, n): return int(n.value)

    def plus_exp(self, l, r): return l + r
    def plus_exp_left(self, l, r): return l + r

    def minus_exp(self, l, r): return l - r
    def minus_exp_left(self, l, r): return l - r

    def times_exp(self, l, r): return l * r
    def times_exp_left(self, l, r): return l * r

    def lt_exp(self, l, r):
        if l < r: return "true"
        return "false"

    def lt_exp_left(self, l, r):
        if l < r: return "true"
        return "false"

    def true_literal(self): return "true"

    def false_literal(self): return "false"
    
    def bool(self, b): return b

    def paren_exp(self, val): return val

    def ite_exp(self, cond, t_operand, f_operand):
        if cond == "true": return t_operand
        else: return f_operand

@v_args(tree=True)
class DerivateEvalNatExp(Interpreter):
    def __init__(self, words):
        super().__init__()
        self.words = words

    def is_form(self, is_form_tree):
        lhs, rhs = is_form_tree.children
        l_operand, r_operand = lhs.children

        # B-Plus
        if lhs.data == "plus_operand":
            if l_operand.get_int() + r_operand.get_int() == rhs.get_int():
                self.words.append(f"{is_form_tree.to_string()} by B-Plus {{}}")
        # B-Minus
        elif lhs.data == "minus_operand":
            if l_operand.get_int() - r_operand.get_int() == rhs.get_int():
                self.words.append(f"{is_form_tree.to_string()} by B-Minus {{}}")
        # B-Times
        elif lhs.data == "times_operand":
            if l_operand.get_int() * r_operand.get_int() == rhs.get_int():
                self.words.append(f"{is_form_tree.to_string()} by B-Times {{}}")
        # B-Lt
        elif lhs.data == "lt_operand":
            if (l_operand.get_int() < r_operand.get_int() and rhs.get_bool_string() == "true") \
               or (l_operand.get_int() >= r_operand.get_int() and rhs.get_bool_string() == "false"):
                self.words.append(f"{is_form_tree.to_string()} by B-Lt {{}}")

    def evalto_form(self, evalto_form_tree):
        lhs, rhs = evalto_form_tree.children
        # E-Int
        if lhs.data == "paren_exp" and lhs.children[0].data == "int":
            self.words.append(f"{evalto_form_tree.to_string()} by E-Int {{}}")

        # E-Bool
        elif lhs.data == "paren_exp" and lhs.children[0].data == "bool":
            self.words.append(f"{evalto_form_tree.to_string()} by E-bool {{}}")
        
        elif lhs.data == "ite_exp":
            cond, t_operand, f_operand = lhs.children
            cond_bool = EvalEvalML1().transform(cond)

            # E-IfT
            if cond_bool == "true":
                self.words.append(f"{evalto_form_tree.to_string()} by E-IfT {{") 
                evalto_form_tree.children = []
                evalto_form_tree.children.extend([
                    Tree("evalto_form", [
                        cond,
                        Tree("bool", [Tree("true_literal", [])])
                    ]),
                    Tree("evalto_form", [
                        t_operand, rhs
                    ])
                ])

            # E-IfF
            elif cond_bool == "false":
                self.words.append(f"{evalto_form_tree.to_string()} by E-IfF {{") 
                evalto_form_tree.children = []
                evalto_form_tree.children.extend([
                    Tree("evalto_form", [
                        cond,
                        Tree("bool", [Tree("false_literal", [])])
                    ]),
                    Tree("evalto_form", [
                        f_operand, rhs
                    ])
                ])

            for i in range(2):
                self.visit(evalto_form_tree.children[i])

                if i < 2: self.words[-1] += ";"

            self.words.append("}")

        
        # (foo op bar) evalto rhs -> foo op bar evalto rhs
        elif lhs.data == "paren_exp":
            evalto_form_tree.children = [
                    lhs.children[0], rhs
            ]
            
            self.visit(evalto_form_tree)

        elif lhs.data in ["plus_exp", "minus_exp", "times_exp", "lt_exp"] \
             or lhs.data in ["plus_exp_left", "minus_exp_left", "times_exp_left", "lt_exp_left"]:
            if lhs.data in ["plus_exp", "minus_exp", "times_exp", "lt_exp"]:
                op = lhs.data[:-4] # "foo_exp" -> "foo"
            else:
                op = lhs.data[:-9] # "foo_exp_left" -> "foo"
            l_operand, r_operand = lhs.children
            l_int = EvalEvalML1().transform(l_operand)
            r_int = EvalEvalML1().transform(r_operand)

            # E-Plus
            if op == "plus":
                self.words.append(f"{evalto_form_tree.to_string()} by E-Plus {{")
            # E-Minus
            elif op == "minus":
                self.words.append(f"{evalto_form_tree.to_string()} by E-Minus {{")
            # E-Times
            elif op == "times":
                self.words.append(f"{evalto_form_tree.to_string()} by E-Times {{")
            # E-Lt
            elif op == "lt":
                self.words.append(f"{evalto_form_tree.to_string()} by E-Lt {{")
            else: raise Exception

            evalto_form_tree.children = []
            evalto_form_tree.children.extend([
                Tree("evalto_form", [
                    l_operand, int_to_tree(l_int)
                ]),
                Tree("evalto_form", [
                    r_operand, int_to_tree(r_int)
                ]),
                Tree("is_form", [
                    Tree(f"{op}_operand", [
                        int_to_tree(l_int),
                        int_to_tree(r_int),
                    ]),
                    rhs
                ])
            ])

            for i in range(3):
                self.visit(evalto_form_tree.children[i])

                if i < 2: self.words[-1] += ";"

            self.words.append("}")