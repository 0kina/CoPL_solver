# 実装途中
from __future__ import annotations
import sys

from lark.tree import Tree
from lark.visitors import Transformer, Interpreter, v_args

from helper import get_int, get_bool, get_val, int_to_tree, to_string

ERROR = "error"

# 引数：構文木
# 返り値：出力する文字列のリスト
def derivate_is_tree(tree: Tree, answer: list):
    if tree.data != "is_form": raise Exception

    lhs, rhs = tree.children
    l_int = int(get_int(lhs.children[0]))
    r_int = int(get_int(lhs.children[1]))
    if lhs.data == "plus_operand":
        rhs_int = int(get_int(rhs))
        if l_int + r_int != rhs_int: raise Exception
        return [f"{to_string(tree)} by B-Plus {{}}"]
    elif lhs.data == "minus_operand":
        rhs_int = int(get_int(rhs))
        if l_int - r_int != rhs_int: raise Exception
        return [f"{to_string(tree)} by B-Minus {{}}"]
    elif lhs.data == "times_operand":
        rhs_int = int(get_int(rhs))
        if l_int * r_int != rhs_int: raise Exception
        return [f"{to_string(tree)} by B-Times {{}}"]
    elif lhs.data == "lt_operand":
        rhs_bool = get_bool(rhs)
        if not (l_int < r_int and rhs_bool == "true" or l_int >= r_int and rhs_bool == "false"):
            raise Exception
        return [f"{to_string(tree)} by B-Lt {{}}"]
    else:
        raise Exception

# 引数：構文木
# 返り値：左辺の評価値（整数を表す文字列 or "true" or "false" or "error"），出力する文字列のリスト
def derivate_eval_tree(tree: Tree) -> tuple[str, list[str]]:
    if tree.data != "eval_form": raise Exception

    lhs, rhs = tree.children
    if lhs.data == "int":
        if get_int(lhs) != get_int(rhs): raise Exception
        return (get_int(lhs), [f"{to_string(tree)} by E-Int {{}}"])

    elif lhs.data == "bool":
        if get_bool(lhs) != get_bool(rhs): raise Exception
        return (get_bool(lhs), [f"{to_string(tree)} by E-Bool {{}}"])

    elif lhs.data == "ite_exp":
        cond, true_exp, false_exp = lhs.children
        cond_val, cond_list = derivate_eval_tree(cond)
        true_val, true_list = derivate_eval_tree(true_exp)
        false_val, false_list = derivate_eval_tree(false_exp)
        if cond_val == "true":
            if true_val == get_val(rhs):
                return (true_val, 
                        [f"{to_string(tree)} by E-IfT {{"] + cond_list + true_list + ["}"])
            elif true_val == ERROR:
                return (ERROR, 
                        [f"{to_string(tree)} by E-IfTError {{"] + cond_list + true_list + ["}"])
            else: raise Exception
        elif cond_val == "false":
            if false_val == get_val(rhs):
                return (false_val, 
                        [f"{to_string(tree)} by E-IfF {{"] + cond_list + false_list + ["}"])
            elif false_val == ERROR:
                return (ERROR, 
                        [f"{to_string(tree)} by E-IfFError {{"] + cond_list + false_list + ["}"])
            else: raise Exception
        elif cond_val.isdigit():
            return (ERROR, 
                    [f"{to_string(tree)} by E-IfInt {{"] + cond_list + ["}"])
        elif cond_val == ERROR:
            return (ERROR, 
                    [f"{to_string(tree)} by E-IfError {{"] + cond_list + ["}"])
        else: raise Exception
    elif lhs.data == "plus_exp":
        l_operand, r_operand = lhs.children
        l_val, l_list = derivate_eval_tree(l_operand)
        r_val, r_list = derivate_eval_tree(r_operand)
        if l_val.isdigit() and r_val.isdigit():
            return (str(int(l_val) + int(r_val)),
                    [f"{to_string(tree)} by E-Plus {{"] + l_list + ["}"])
    # elif lhs.data in ["plus_exp", "minus_exp", "times_exp", "lt_exp"] \
    #      or lhs.data in ["plus_exp_left", "minus_exp_left", "times_exp_left", "lt_exp_left"]:
    #     if lhs.data in ["plus_exp", "minus_exp", "times_exp", "lt_exp"]:
    #         op = lhs.data[:-4] # "foo_exp" -> "foo"
    #     else:
    #         op = lhs.data[:-9] # "foo_exp_left" -> "foo"


    elif lhs.data == "paren_exp":
        return derivate_eval_tree(lhs.children[0])

    else: raise Exception

def eval_exp(tree: Tree) -> str:
    if tree.data == "int": return get_int(tree)
    elif tree.data == "bool": return get_bool(tree)
    else: raise Exception



# @v_args(inline=True)
# class EvalEvalML1(Transformer):
#     def __default__(self, data, children, meta): raise Exception

#     def int(self, n): return int(n.value)

#     def plus_exp(self, l, r):
#         if l in ["true", "false", "error"] or r in ["true", "false", "error"]:
#             return "error"
#         else:
#             return l + r

#     def plus_exp_left(self, l, r):
#         if l in ["true", "false", "error"] or r in ["true", "false", "error"]:
#             return "error"
#         else:
#             return l + r

#     def minus_exp(self, l, r):
#         if l in ["true", "false", "error"] or r in ["true", "false", "error"]:
#             return "error"
#         else:
#             return l - r

#     def minus_exp_left(self, l, r):
#         if l in ["true", "false", "error"] or r in ["true", "false", "error"]:
#             return "error"
#         else:
#             return l - r

#     def times_exp(self, l, r):
#         if l in ["true", "false", "error"] or r in ["true", "false", "error"]:
#             return "error"
#         else:
#             return l * r

#     def times_exp_left(self, l, r):
#         if l in ["true", "false", "error"] or r in ["true", "false", "error"]:
#             return "error"
#         else:
#             return l * r

#     def lt_exp(self, l, r):
#         if l in ["true", "false", "error"] or r in ["true", "false", "error"]:
#             return "error"
#         elif l < r: return "true"
#         return "false"

#     def lt_exp_left(self, l, r):
#         if l in ["true", "false", "error"] or r in ["true", "false", "error"]:
#             return "error"
#         elif l < r: return "true"
#         return "false"

#     def true_literal(self): return "true"

#     def false_literal(self): return "false"
    
#     def bool(self, b): return b

#     def paren_exp(self, val): return val

#     def ite_exp(self, cond, t_operand, f_operand):
#         if cond not in ["true", "false"]: return "error"
#         elif cond == "true":
#             if t_operand == "error": return "error"
#             return t_operand
#         else:
#             if f_operand == "error": return "error"
#             return f_operand

# @v_args(tree=True)
# class DerivateEvalNatExp(Interpreter):
#     def __init__(self, words):
#         super().__init__()
#         self.words = words

#     def is_form(self, is_form_tree):
#         lhs, rhs = is_form_tree.children
#         l_operand, r_operand = lhs.children

#         # B-Plus
#         if lhs.data == "plus_operand":
#             if l_operand.get_int() + r_operand.get_int() == rhs.get_int():
#                 self.words.append(f"{is_form_tree.to_string()} by B-Plus {{}}")
#         # B-Minus
#         elif lhs.data == "minus_operand":
#             if l_operand.get_int() - r_operand.get_int() == rhs.get_int():
#                 self.words.append(f"{is_form_tree.to_string()} by B-Minus {{}}")
#         # B-Times
#         elif lhs.data == "times_operand":
#             if l_operand.get_int() * r_operand.get_int() == rhs.get_int():
#                 self.words.append(f"{is_form_tree.to_string()} by B-Times {{}}")
#         # B-Lt
#         elif lhs.data == "lt_operand":
#             if (l_operand.get_int() < r_operand.get_int() and rhs.get_bool_string() == "true") \
#                or (l_operand.get_int() >= r_operand.get_int() and rhs.get_bool_string() == "false"):
#                 self.words.append(f"{is_form_tree.to_string()} by B-Lt {{}}")

#     def evalto_form(self, evalto_form_tree):
#         lhs, rhs = evalto_form_tree.children
#         # E-Int
#         if lhs.data == "paren_exp" and lhs.children[0].data == "int":
#             self.words.append(f"{evalto_form_tree.to_string()} by E-Int {{}}")

#         # E-Bool
#         elif lhs.data == "paren_exp" and lhs.children[0].data == "bool":
#             self.words.append(f"{evalto_form_tree.to_string()} by E-bool {{}}")
        
#         elif lhs.data == "ite_exp":
#             cond, t_operand, f_operand = lhs.children
#             cond_bool = EvalEvalML1().transform(cond)

#             # E-IfT
#             if cond_bool == "true":
#                 self.words.append(f"{evalto_form_tree.to_string()} by E-IfT {{") 
#                 evalto_form_tree.children = []
#                 evalto_form_tree.children.extend([
#                     Tree("evalto_form", [
#                         cond,
#                         Tree("bool", [Tree("true_literal", [])])
#                     ]),
#                     Tree("evalto_form", [
#                         t_operand, rhs
#                     ])
#                 ])

#             # E-IfF
#             elif cond_bool == "false":
#                 self.words.append(f"{evalto_form_tree.to_string()} by E-IfF {{") 
#                 evalto_form_tree.children = []
#                 evalto_form_tree.children.extend([
#                     Tree("evalto_form", [
#                         cond,
#                         Tree("bool", [Tree("false_literal", [])])
#                     ]),
#                     Tree("evalto_form", [
#                         f_operand, rhs
#                     ])
#                 ])

#             for i in range(2):
#                 self.visit(evalto_form_tree.children[i])

#                 if i < 2: self.words[-1] += ";"

#             self.words.append("}")

        
#         # (foo op bar) evalto rhs -> foo op bar evalto rhs
#         elif lhs.data == "paren_exp":
#             evalto_form_tree.children = [
#                     lhs.children[0], rhs
#             ]
            
#             self.visit(evalto_form_tree)

#         elif lhs.data in ["plus_exp", "minus_exp", "times_exp", "lt_exp"] \
#              or lhs.data in ["plus_exp_left", "minus_exp_left", "times_exp_left", "lt_exp_left"]:
#             if lhs.data in ["plus_exp", "minus_exp", "times_exp", "lt_exp"]:
#                 op = lhs.data[:-4] # "foo_exp" -> "foo"
#             else:
#                 op = lhs.data[:-9] # "foo_exp_left" -> "foo"
#             l_operand, r_operand = lhs.children
#             l_int = EvalEvalML1().transform(l_operand)
#             r_int = EvalEvalML1().transform(r_operand)

#             # E-Plus
#             if op == "plus":
#                 self.words.append(f"{evalto_form_tree.to_string()} by E-Plus {{")
#             # E-Minus
#             elif op == "minus":
#                 self.words.append(f"{evalto_form_tree.to_string()} by E-Minus {{")
#             # E-Times
#             elif op == "times":
#                 self.words.append(f"{evalto_form_tree.to_string()} by E-Times {{")
#             # E-Lt
#             elif op == "lt":
#                 self.words.append(f"{evalto_form_tree.to_string()} by E-Lt {{")
#             else: raise Exception

#             evalto_form_tree.children = []
#             evalto_form_tree.children.extend([
#                 Tree("evalto_form", [
#                     l_operand, int_to_tree(l_int)
#                 ]),
#                 Tree("evalto_form", [
#                     r_operand, int_to_tree(r_int)
#                 ]),
#                 Tree("is_form", [
#                     Tree(f"{op}_operand", [
#                         int_to_tree(l_int),
#                         int_to_tree(r_int),
#                     ]),
#                     rhs
#                 ])
#             ])

#             for i in range(3):
#                 self.visit(evalto_form_tree.children[i])

#                 if i < 2: self.words[-1] += ";"

#             self.words.append("}")