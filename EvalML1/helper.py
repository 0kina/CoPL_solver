from lark import Tree, Token

def pretty(words):
    ret = []
    indent = 0
    for word in words:
        if word == "}" or word == "};": indent -= 1

        ret.append(f"{'  ' * indent}{word}")

        if word[-1] == "{": indent += 1

    return "\n".join(ret)


def int_to_tree(n):
    return Tree(Token('RULE', 'int'), [Token('SIGNED_INT', str(n))])

def bool_to_tree(n):
    return Tree(Token('RULE', 'bool'), [Token('SIGNED_INT', str(n))])

def to_string(t):
    if t.data == "plus_literal": return "plus"
    elif t.data == "minus_literal": return "minus"
    elif t.data == "times_literal": return "times"
    elif t.data == "true_literal": return "true"
    elif t.data == "false_literal": return "false"
    elif t.data == "evalto_literal": return "evalto"
    elif t.data == "plus_op": return "+"
    elif t.data == "minus_op": return "-"
    elif t.data == "times_op": return "*"
    elif t.data == "lt_op": return "<"
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
    elif t.data == "int": return str(t.get_int())
    elif t.data == "bool": return t.get_bool_string()
    else:
        return " ".join([to_string(sub_tree) for sub_tree in t.children])

Tree.to_string = to_string

def get_int(t):
    if t.data != "int":
        raise Exception
    return int(t.children[0].value)

Tree.get_int = get_int

def get_bool_string(t):
    if t.data != "bool":
        raise Exception
    if t.children[0].data == "true_literal": return "true"
    else: return "false"

Tree.get_bool_string = get_bool_string