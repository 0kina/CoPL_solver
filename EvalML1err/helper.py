from __future__ import annotations

from typing import Union

from lark.lexer import Token
from lark.tree import Tree

from typeguard import check_type

from eval_ml1_err_types import t_node, t_int, t_bool, t_val

def pretty(words) -> str:
    ret = []
    indent = 0
    for word in words:
        if word == "}" or word == "};": indent -= 1

        ret.append(f"{'  ' * indent}{word}")

        if word[-1] == "{": indent += 1

    return "\n".join(ret)


def int_to_tree(n: str) -> Tree:
    return Tree("int", [Token("SIGNED_INT", n)])

def bool_to_tree(tf: str) -> Tree:
    if tf == "true":
        return Tree("bool", [Tree(tf + "_literal", [])])
    elif tf == "false":
        return Tree("bool", [Tree(tf + "_literal", [])])
    else: raise Exception

def make_is_form(l_operand: str, op: str, r_operand: str) -> Tree:
    if op == "plus":
        rhs = str(int(l_operand) + int(r_operand))
        return Tree("is_form", [Tree("plus_operand", [int_to_tree(l_operand), int_to_tree(r_operand)]), \
                                int_to_tree(rhs)])

    elif op == "minus":
        rhs = str(int(l_operand) - int(r_operand))
        return Tree("is_form", [Tree("minus_operand", [int_to_tree(l_operand), int_to_tree(r_operand)]), \
                                int_to_tree(rhs)])

    elif op == "times":
        rhs = str(int(l_operand) * int(r_operand))
        return Tree("is_form", [Tree("times_operand", [int_to_tree(l_operand), int_to_tree(r_operand)]), \
                                int_to_tree(rhs)])

    elif op == "lt":
        if int(l_operand) < int(r_operand): rhs = "true"
        else: rhs = "false"
        return Tree("is_form", [Tree("lt_operand", [int_to_tree(l_operand), int_to_tree(r_operand)]), \
                                bool_to_tree(rhs)])
    else: raise Exception

def make_evalto_form(lhs: Tree, rhs: str) -> Tree:
    return Tree("evalto_form", [lhs, int_to_tree(rhs)])

def to_string(t: Tree) -> str:
    if t.data == "true_literal": return "true"
    elif t.data == "false_literal": return "false"
    elif t.data == "paren_exp" and t.children[0].data not in ["int", "bool"] :
        return "(" + to_string(t.children[0]) + ")"
    elif t.data == "is_form":
        return " ".join([to_string(t.children[0]), "is", to_string(t.children[1])])
    elif t.data == "plus_operand":
        return " ".join([to_string(t.children[0]), "plus", to_string(t.children[1])])
    elif t.data == "minus_operand":
        return " ".join([to_string(t.children[0]), "minus", to_string(t.children[1])])
    elif t.data == "times_operand":
        return " ".join([to_string(t.children[0]), "times", to_string(t.children[1])])
    elif t.data == "lt_operand":
        return " ".join([to_string(t.children[0]), "less than", to_string(t.children[1])])
    elif t.data == "ite_exp":
        return " ".join(["if", to_string(t.children[0]), "then", to_string(t.children[1]),
                         "else", to_string(t.children[2])])
    elif t.data in ["plus_exp", "plus_exp_left"]:
        return " ".join([to_string(t.children[0]), "+", to_string(t.children[1])])
    elif t.data in ["minus_exp", "minus_exp_left"]:
        return " ".join([to_string(t.children[0]), "-", to_string(t.children[1])])
    elif t.data in ["times_exp", "times_exp_left"]:
        return " ".join([to_string(t.children[0]), "*", to_string(t.children[1])])
    elif t.data in ["lt_exp", "lt_exp_left"]:
        return " ".join([to_string(t.children[0]), "<", to_string(t.children[1])])
    elif t.data == "evalto_form":
        return " ".join([to_string(t.children[0]), "evalto", to_string(t.children[1])])
    elif t.data == "int": return str(get_int(t))
    elif t.data == "bool": return get_bool(t)
    else:
        return " ".join([to_string(sub_tree) for sub_tree in t.children])

def get_int(t: Tree) -> t_int:
    if t.data != "int":
        raise Exception
    return int(t.children[0].value)  # type: ignore

def get_bool(t: Tree) -> t_bool:
    if t.data != "bool":
        raise Exception
    if t.children[0].data == "true_literal": return "true"
    else: return "false"

def get_val(t) -> t_val:
    if t.data == "int": return get_int(t)
    elif t.data == "bool": return get_bool(t)
    elif t.data == "error_literal": return "error"
    else: raise Exception

def calc_val(node: t_node, children: list[t_val]) -> t_val:
    if node in ["int", "true", "false"]: return children[0]
    elif node in ["plus", "minus", "times"]:
        l_operand, r_operand = children
        try:
            check_type("l_operand", l_operand, t_int)
            check_type("r_operand", r_operand, t_int)
            if node == "plus":
                return l_operand + r_operand # type: ignore
            elif node == "minus":
                return l_operand - r_operand # type: ignore
            else:
                return l_operand * r_operand # type: ignore
        except TypeError:
            return "error"
    elif node == "lt":
        l_operand, r_operand = children
        try:
            check_type("l_operand", l_operand, t_int)
            check_type("r_operand", r_operand, t_int)
            if l_operand < r_operand: return "true" # type: ignore
            else: return "false"
        except TypeError:
            return "error"
    elif node == "ite":
        cond, t_operand, f_operand = children
        try:
            check_type("cond", cond, t_bool)
            if cond == "true":
                check_type("t_operand", t_operand, Union[t_int, t_bool])
                return t_operand
            else:
                check_type("f_operand", f_operand, Union[t_int, t_bool])
                return f_operand
        except TypeError:
            return "error"
    elif node == "par":
        return children[0]
    else: raise Exception