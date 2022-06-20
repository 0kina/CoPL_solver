from lark.lexer import Token
from lark.tree import Tree

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
        print("asdf")
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
    elif t.data == "int": return get_int(t)
    elif t.data == "bool": return get_bool(t)
    else:
        return " ".join([to_string(sub_tree) for sub_tree in t.children])

def get_int(t: Tree) -> str:
    if t.data != "int":
        raise Exception
    return t.children[0].value  # type: ignore

def get_bool(t: Tree) -> str:
    if t.data != "bool":
        raise Exception
    if t.children[0].data == "true_literal": return "true"
    else: return "false"

def get_val(t) -> str:
    if t.data == "int": return get_int(t)
    elif t.data == "bool": return get_bool(t)
    else: raise Exception