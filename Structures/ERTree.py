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
        levels = [1] * len(ps)
        aux = [0] * len(ps)
        add_value = 0

        for i in range(len(ps)):
            if (ps[i] == ")"):
                aux[i] -= add_value
                add_value -= 1

            levels[i] += add_value

            if (ps[i] == "("):
                add_value += 1
                aux[i] += add_value

            if (ps[i] == "|"):
                aux[i] = "|"

            if (ps[i] == "*"):
                # levels[i] += 1
                # levels[i] *= -1
                aux[i] = "*"

        rps = list(reversed(ps))
        rlevels = list(reversed(levels))
        raux = list(reversed(aux))

        concats = [i for i, x in enumerate(rlevels) if x == 1]
        unions = get_char_on_level("|", levels, aux)

        gvalues = []

        rclosures = get_char_on_level("*", rlevels, raux)

        operation = None

        if len(unions) > 0:
            operation = "|"
            gvalues = [ps[:unions[-1]], ps[unions[-1]+1:]]
        elif raux[0] == "*" and raux[1] == 0:
            operation = "*"
            gvalues = [ps[:-1]]
        elif raux[0] == "*" and raux.index(1) + 1 == len(raux):
            operation = "*"
            gvalues = [ps[1:-2]]
        else:
            operation = "."
            for i, g in enumerate(concats):
                if raux[g] == 0 or (raux[g] == "*" and raux[g+1] == 0):
                    if len(gvalues) == 1:
                        gvalues.insert(0, ''.join(reversed(rps[g:])))
                        break
                    else:
                        gvalues.insert(0, rps[g])
                else:
                    if raux[g] == -1:
                        if g-1 in rclosures:
                            gvalues.insert(0, ''.join(
                                reversed(rps[g-1:concats[i+1]+1])))
                        else:
                            gvalues.insert(0, ''.join(
                                reversed(rps[g+1:concats[i+1]])))
                    else:
                        continue

        if (len(gvalues) == 2):
            gvalues = Node(
                operation,
                Node(gvalues[0])
                if len(gvalues[0]) == 1 else self.split_expression(gvalues[0]),
                Node(gvalues[1])
                if len(gvalues[1]) == 1 else self.split_expression(gvalues[1])
            )
        else:
            if operation is None:
                gvalues = Node(gvalues[0])
            else:
                gvalues = Node(
                    operation,
                    Node(gvalues[0])
                    if len(gvalues[0]) == 1 else self.split_expression(gvalues[0])
                )

        return gvalues


# (aa|ba)#
