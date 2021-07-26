from DEFINITIONS import *


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
        self.parent = None

        self.nodes = [node_1, node_2]

    def leaf(self):
        return not any(self.nodes)

    def set_parent(self, parent=None):
        self.parent = parent
        if self.leaf():
            return
        else:
            if self.value == CLOSURE:
                self.nodes[0].set_parent(self)
                return
            else:
                self.nodes[0].set_parent(self)
                self.nodes[1].set_parent(self)
                return

    def get_followpos_changer(self):
        if self.value == ".":
            return [self] + self.nodes[0].get_followpos_changer() + self.nodes[1].get_followpos_changer()
        elif self.value == "*":
            return [self] + self.nodes[0].get_followpos_changer()
        elif self.value == "|":
            return [] + self.nodes[0].get_followpos_changer()
        else:
            return []

    def get_leaves(self):
        if self.leaf():
            return [self]
        else:
            if self.value == CLOSURE:
                return self.nodes[0].get_leaves()
            else:
                return self.nodes[0].get_leaves() + self.nodes[1].get_leaves()

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
                return any(map(lambda x: x.nullable(), self.nodes))
            elif self.value == CONCAT:
                return all(map(lambda x: x.nullable(), self.nodes))
            elif self.value == CLOSURE:
                return True
        return False

    def firstpos(self):
        if self.leaf():
            if self.value == EPSILON:
                return []
            else:
                return [self]
        else:
            if self.value == UNION:
                return self.nodes[0].firstpos() + self.nodes[1].firstpos()
            elif self.value == CONCAT:
                if self.nodes[0].nullable():
                    return self.nodes[0].firstpos() + self.nodes[1].firstpos()
                else:
                    return self.nodes[0].firstpos()
            elif self.value == CLOSURE:
                return self.nodes[0].firstpos()
        return []

    def lastpos(self):
        if self.leaf():
            if self.value == EPSILON:
                return []
            else:
                return [self]
        else:
            if self.value == UNION:
                return self.nodes[0].lastpos() + self.nodes[1].lastpos()
            elif self.value == CONCAT:
                if self.nodes[1].nullable():
                    return self.nodes[0].lastpos() + self.nodes[1].lastpos()
                else:
                    return self.nodes[1].lastpos()
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

    def __lt__(self, other):
        return self.nid < other.nid


class ERTree:

    def __init__(self):
        self.root = None

    def pretty_print(self):
        self.root.pretty_print()

    def create_tree(self, ps):
        self.root = self.split_expression(f"({ps})#")
        self.root.set_parent()
        leaves = self.get_leaves()
        count = 0
        for l in leaves:
            count += 1
            l.nid = count
        followpos_nodes = self.root.get_followpos_changer()
        return (leaves, followpos_nodes)

    def split_expression(self, ps):
        if (len(ps) == 1 or ps == "a-z" or ps == "A-Z" or ps == "0-9"):
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
            elif rps[i] in "-" and i >= 1 and i <= len(rps) - 2 and cur_level == 1 and rps[i-1] not in "(|)*" and rps[i+1] not in "(|)*":
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
            if (zipped[1] == (1, "-")):
                items.insert(0, ''.join(reversed(rps[:3])))
                end += 2
            else:
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

    def get_leaves(self):
        return self.root.get_leaves()

    def flat_tree(self):
        return self.root.get_node_array()

# (aa|ba)#
