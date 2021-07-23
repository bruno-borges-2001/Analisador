CONCAT = "."
UNION = "|"
CLOSURE = "*"
EPSILON = "&"
EOS = "#"


def get_char_on_level(char, levels, aux):
    unions = []
    current_level = 1
    for i in range(len(levels)):
        current_level = levels[i]
        if aux[i] == char and current_level == 1:
            unions.append(i)
    return unions


class Node:

    def __init__(self, value, node_1=None, node_2=None, root=False):
        self.nid = str(id(self))
        self.value = value

        self.nodes = [node_1, node_2]
        self.root = root

    def id(self):
        return self.nid

    def leaf(self):
        return not any(self.nodes)

    def fixed(self):
        if self.leaf():
            return [] if len(self.value) == 1 else [self]
        else:
            result = [] if len(self.value) == 1 else [self]
            if self.nodes[0] is not None:
                result += self.nodes[0].fixed()
            if self.nodes[1] is not None:
                result += self.nodes[1].fixed()
            return result

    def __str__(self):
        return self.value


class ERTree:

    def __init__(self):
        self.root = None

    def pretty_print(self, node, level=0, last=False):
        string = " " * (level - 1) * 4
        if level > 0:
            string += ("╚" if last else "╠") + "═" * 2 + " "
            for x in range(0, len(string) - 3, 4):
                if string[x] != " ":
                    continue
                elif x == 0:
                    string = "║" + string[1:]
                else:
                    string = string[:x] + "║" + string[x+1:]
        string += str(node)
        print(string)
        new_level = level + 1
        if node.nodes[0] is not None:
            self.pretty_print(node.nodes[0], new_level, node.nodes[1] is None)
        if node.nodes[1] is not None:
            self.pretty_print(node.nodes[1], new_level, True)

    def create_tree(self, ps):
        self.root = self.split_expression(f"({ps})#")

    def split_expression(self, ps):
        if (len(ps) == 1):
            return Node(ps)

        cur_level = 1
        levels = []
        aux = []

        rps = list(reversed(ps))

        for i in range(len(rps)):
            if (rps[i] == "("):
                cur_level -= 1

            if rps[i] == "|" and cur_level == 1:
                return Node(
                    "|",
                    self.split_expression(''.join(reversed(rps[i+1:]))),
                    self.split_expression(''.join(reversed(rps[:i])))
                )
            elif rps[i] == "*" and cur_level == 1:
                aux.append("*")
            elif rps[i] in "()" and cur_level == 1:
                aux.append(rps[i])
            else:
                aux.append(0)

            levels.append(cur_level)

            if (rps[i] == ")"):
                cur_level += 1

        zipped = list(zip(levels, aux))

        items = []

        end = 0

        if (zipped[0] == (1, 0)):
            items.insert(0, rps[0])
        elif (zipped[0] == (1, ")")):
            end = zipped.index((1, "("))
            items.insert(0, ''.join(reversed(rps[1:end])))
        elif (zipped[0] == (1, "*")):
            if (zipped[1] == (1, ")")):
                end = zipped.index((1, "("))
                if end == len(zipped) - 1:
                    return Node("*", self.split_expression(''.join(reversed(rps[2:-1]))))
                else:
                    items.insert(0, ''.join(reversed(rps[:end+1])))
            else:
                end = 1
                items.insert(0, ''.join(reversed(rps[:end+1])))

        end += 1

        if (zipped[end] == (1, ")")):
            new_end = zipped.index((1, "("), end)
            if (new_end == len(zipped) - 1):
                items.insert(0, ''.join(reversed(rps[end+1:-1])))
            else:
                items.insert(0, ''.join(reversed(rps[end:])))
        else:
            items.insert(0, ''.join(reversed(rps[end:])))

        return Node(".", self.split_expression(items[0]), self.split_expression(items[1]))


# (aa|ba)#
