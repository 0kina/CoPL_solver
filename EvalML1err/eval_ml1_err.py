from __future__ import annotations
from typing import Union

from lark.tree import Tree

from typeguard import check_type

from helper import get_int, get_bool, get_val, calc_val, to_string
from eval_ml1_err_types import t_node, t_int, t_bool, t_val

class EvalTree:
    def __init__(self, node: t_node, children: list[EvalTree], val: Union[None, t_int, t_bool]=None):
        self.node: t_node = node
        self.children: list[EvalTree] = children

        if node == "int":
            check_type("val", val, t_int)
            self.val: t_val = val # type: ignore
            self.tree_string: str = str(self.val)
        elif node == "bool":
            check_type("val", val, t_bool)
            self.val: t_val = val # type: ignore
            self.tree_string: str = str(self.val)
        elif node == "error":
            self.val: t_val = "error"
            self.tree_string: str = str(self.val)
        elif node == "par":
            self.val: t_val = children[0].val
            c_node = children[0].node
            if c_node in ["int", "bool", "error"]:
                self.tree_string: str = children[0].tree_string
            else:
                self.tree_string:str = f"({children[0].tree_string})"
        elif node in ["plus", "minus", "times", "lt", "ite"]:
            children_val: list[t_val] = [child.val for child in children]
            self.val: t_val = calc_val(node, children_val)
            if node == "plus":
                self.tree_string:str = f"{children[0].tree_string} + {children[1].tree_string}"
            elif node == "minus":
                self.tree_string:str = f"{children[0].tree_string} - {children[1].tree_string}"
            elif node == "times":
                self.tree_string:str = f"{children[0].tree_string} * {children[1].tree_string}"
            elif node == "lt":
                self.tree_string:str = f"{children[0].tree_string} < {children[1].tree_string}"
            elif node == "ite":
                self.tree_string:str \
                  = f"if {children[0].tree_string} " \
                    + f"then {children[1].tree_string} else {children[2].tree_string}"
        else:
            raise Exception

def construct_eval_tree(tree: Tree) -> EvalTree:
    if tree.data == "int":
        return EvalTree("int", [], get_int(tree))
    elif tree.data == "bool":
        return EvalTree("bool", [], get_bool(tree))
    elif tree.data == "error_literal":
        return EvalTree("error", [])
    elif tree.data in ["plus_exp", "plus_exp_left"]:
        l_operand, r_operand = tree.children
        l_tree = construct_eval_tree(l_operand)
        r_tree = construct_eval_tree(r_operand)
        return EvalTree("plus", [l_tree, r_tree])
    elif tree.data in ["minus_exp", "minus_exp_left"]:
        l_operand, r_operand = tree.children
        l_tree = construct_eval_tree(l_operand)
        r_tree = construct_eval_tree(r_operand)
        return EvalTree("minus", [l_tree, r_tree])
    elif tree.data in ["times_exp", "times_exp_left"]:
        l_operand, r_operand = tree.children
        l_tree = construct_eval_tree(l_operand)
        r_tree = construct_eval_tree(r_operand)
        return EvalTree("times", [l_tree, r_tree])
    elif tree.data in ["lt_exp", "lt_exp_left"]:
        l_operand, r_operand = tree.children
        l_tree = construct_eval_tree(l_operand)
        r_tree = construct_eval_tree(r_operand)
        return EvalTree("lt", [l_tree, r_tree])
    elif tree.data == "par_exp":
        child_tree = construct_eval_tree(tree.children[0])
        return EvalTree("par", [child_tree])
    elif tree.data == "ite_exp":
        cond, t_operand, f_operand = tree.children
        cond_tree = construct_eval_tree(cond)
        t_tree = construct_eval_tree(t_operand)
        f_tree = construct_eval_tree(f_operand)
        return EvalTree("ite", [cond_tree, t_tree, f_tree])
    else:
        raise Exception

# def make_is_string

def derivate_is_form(judge: Tree):
    lhs, rhs = judge.children
    l_int = int(get_int(lhs.children[0]))
    r_int = int(get_int(lhs.children[1]))
    if lhs.data == "plus_operand":
        rhs_int = int(get_int(rhs))
        if l_int + r_int != rhs_int: raise Exception
        return [f"{to_string(judge)} by B-Plus {{}}"]
    elif lhs.data == "minus_operand":
        rhs_int = int(get_int(rhs))
        if l_int - r_int != rhs_int: raise Exception
        return [f"{to_string(judge)} by B-Minus {{}}"]
    elif lhs.data == "times_operand":
        rhs_int = int(get_int(rhs))
        if l_int * r_int != rhs_int: raise Exception
        return [f"{to_string(judge)} by B-Times {{}}"]
    elif lhs.data == "lt_operand":
        rhs_bool = get_bool(rhs)
        if not (l_int < r_int and rhs_bool == "true" or l_int >= r_int and rhs_bool == "false"):
            raise Exception
        return [f"{to_string(judge)} by B-Lt {{}}"]
    else:
        raise Exception

def derivate_eval_tree(tree: EvalTree) -> list[str]:
    if tree.node == "int":
        return [f"{tree.tree_string} evalto {tree.val} by E-Int {{}}"]

    elif tree.node == "bool":
        return [f"{tree.tree_string} evalto {tree.val} by E-Bool {{}}"]

    elif tree.node in ["plus", "minus", "times", "lt"]:
        l_operand, r_operand = tree.children
        op_name = tree.node.capitalize()

        op = tree.node
        if op == "lt": op = "less than"

        if type(l_operand.val) == t_int and type(r_operand.val) == t_int:
            ret = [f"{tree.tree_string} evalto {tree.val} by E-{op_name} {{"]
            ret.extend(derivate_eval_tree(l_operand))
            ret[-1] += ";"
            ret.extend(derivate_eval_tree(r_operand))
            ret[-1] += ";"
            ret.append(f"{l_operand.val} {op} {r_operand.val} is {tree.val} by B-{op_name} {{}}")
            ret.append("}")
        elif l_operand.val in ["true", "false"]:
            ret = [f"{tree.tree_string} evalto {tree.val} by E-{op_name}BoolL {{"]
            ret.extend(derivate_eval_tree(l_operand))
            ret.append("}")
        elif r_operand.val in ["true", "false"]:
            ret = [f"{tree.tree_string} evalto {tree.val} by E-{op_name}BoolR {{"]
            ret.extend(derivate_eval_tree(r_operand))
            ret.append("}")
        elif l_operand.val == "error":
            ret = [f"{tree.tree_string} evalto {tree.val} by E-{op_name}ErrorL {{"]
            ret.extend(derivate_eval_tree(l_operand))
            ret.append("}")
        elif r_operand.val == "error":
            ret = [f"{tree.tree_string} evalto {tree.val} by E-{op_name}ErrorR {{"]
            ret.extend(derivate_eval_tree(r_operand))
            ret.append("}")
        else: raise Exception

        return ret

    elif tree.node == "ite":
        cond, t_operand, f_operand = tree.children
        if cond.val == "true":
            if t_operand.val != "error":
                ret = [f"{tree.tree_string} evalto {tree.val} by E-IfT {{"]
            else:
                ret = [f"{tree.tree_string} evalto {tree.val} by E-IfTError {{"]
            ret.extend(derivate_eval_tree(cond))
            ret[-1] += ";"
            ret.extend(derivate_eval_tree(t_operand))
            ret.append("}")
        elif cond.val == "false":
            if f_operand.val != "error":
                ret = [f"{tree.tree_string} evalto {tree.val} by E-IfF {{"]
            else:
                ret = [f"{tree.tree_string} evalto {tree.val} by E-IfFError {{"]
            ret.extend(derivate_eval_tree(cond))
            ret[-1] += ";"
            ret.extend(derivate_eval_tree(f_operand))
            ret.append("}")
        elif type(cond.val) == t_int:
            ret = [f"{tree.tree_string} evalto {tree.val} by E-IfInt {{"]
            ret.extend(derivate_eval_tree(cond))
            ret.append("}")
        elif cond.val == "error":
            ret = [f"{tree.tree_string} evalto {tree.val} by E-IfError {{"]
            ret.extend(derivate_eval_tree(cond))
            ret.append("}")
        else:
            raise Exception

        return ret

    elif tree.node == "par":
        return derivate_eval_tree(tree.children[0])
    else: raise Exception

from helper import pretty

def derivate(judge: Tree) -> None:
    if judge.data == "is_form": derivate_is_form(judge)
    elif judge.data == "evalto_form":
        lhs, rhs = judge.children
        lhs_tree = construct_eval_tree(lhs)
        rhs_val = get_val(rhs)

        if lhs_tree.val != rhs_val:
            raise Exception

        answer_list = derivate_eval_tree(lhs_tree)
        print(pretty(answer_list))

    # lhs, rhs = judge.children
    # if judge.data == "is_form":
    #     if lhs.data == "plus_operand":
    else: raise Exception