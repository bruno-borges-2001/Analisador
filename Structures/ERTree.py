CONCAT = "."
UNION = "|"
CLOSURE = "*"
EPSILON = "&"


def get_char_on_level(char, levels, aux):
    unions = []
    current_level = 1
    for i in range(len(levels)):
        current_level = levels[i]
        if aux[i] == char and current_level == 1:
            unions.append(i)
    return unions


class Node:

    def __init__(self, value, node_1=None, node_2=None):
        self.value = value
        self.nid = 0

        self.nodes = [node_1, node_2]

    def leaf(self):
        return not any(self.nodes)

    def get_leafs(self):
        if self.leaf():
            return [self]
        else:
            if self.value == CLOSURE:
                return self.nodes[0].get_leafs()
            else:
                return self.nodes[0].get_leafs() + self.nodes[1].get_leafs()

    def get_node_array(self):
        if self.leaf():
            return [self]
        else:
            if self.value == CLOSURE:
                return [self] + self.nodes[0].get_node_array()
            else:
                return [self] + self.nodes[0].get_node_array() + self.nodes[1].get_node_array()

    def nullable(self):
        if self.leaf():
            return self.value == EPSILON
        else:
            if self.value == UNION:
                return any(map(lambda x: x.nullable, self.nodes))
            elif self.value == CONCAT:
                return all(map(lambda x: x.nullable, self.nodes))
            elif self.value == CLOSURE:
                return True
        return False

    def firstpos(self):
        if self.leaf():
            if self.value == EPSILON:
                return []
            else:
                return [self.value]
        else:
            if self.value == UNION:
                return self.nodes[0].firstpos() + self.nodes[1].firstpos()
            elif self.value == CONCAT:
                if self.nodes[0].nullable():
                    self.nodes[0].firstpos() + self.nodes[1].firstpos()
                else:
                    self.nodes[0].firstpos()
            elif self.value == CLOSURE:
                return self.nodes[0].firstpos()
        return []

    def lastpos(self):
        if self.leaf():
            if self.value == EPSILON:
                return []
            else:
                return [self.value]
        else:
            if self.value == UNION:
                return self.nodes[0].lastpos() + self.nodes[1].lastpos()
            elif self.value == CONCAT:
                if self.nodes[1].nullable():
                    self.nodes[0].lastpos() + self.nodes[1].lastpos()
                else:
                    self.nodes[1].lastpos()
            elif self.value == CLOSURE:
                return self.nodes[0].lastpos()
        return []

    def pretty_print(self, level=0, last=[]):
        string = " " * (level - 1) * 4
        if level > 0:
            string += ("╚" if len(last) >
                       0 and last[-1] == level-1 else "╠") + "═" * 2 + " "
            for x in range(0, len(string) - 3, 4):
                if string[x] != " ":
                    continue
                elif x == 0:
                    string = "║" + string[1:]
                elif x / 4 not in last:
                    string = string[:x] + "║" + string[x+1:]
        string += self.value
        print(string)
        new_level = level + 1
        new_last = [] + last
        if self.nodes[0] is not None:
            if self.nodes[1] is None:
                new_last += [level]
            self.nodes[0].pretty_print(new_level, new_last)
        if self.nodes[1] is not None:
            new_last += [level]
            self.nodes[1].pretty_print(new_level, new_last)

    def __str__(self):
        return self.value


class ERTree:

    def __init__(self):
        self.root = None

    def pretty_print(self):
        self.root.pretty_print()

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

    def get_leafs(self):
        return self.root.get_leafs()

    def flat_tree(self):
        return self.root.get_node_array()

# (aa|ba)#
