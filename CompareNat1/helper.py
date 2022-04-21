from lark import Tree

def int_to_tree(n):
    if n == 0:
        return Tree("zero", [])
    else:
        return Tree("succ", [int_to_tree(n - 1)])

def pretty(words):
    ret = []
    indent = 0
    for word in words:
        if word == "}" or word == "};": indent -= 1

        ret.append(f"{'  ' * indent}{word}")

        if word[-1] == "{": indent += 1

    return "\n".join(ret)

def to_string(t):
    if t.data == "zero": return "Z"
    elif t.data == "succ": return "S(" + to_string(t.children[0]) + ")"
    elif t.data == "lt_literal": return "is less than"
    else:
        return " ".join([to_string(sub_tree) for sub_tree in t.children])

Tree.to_string = to_string