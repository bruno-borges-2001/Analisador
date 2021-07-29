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
        if self.leaf():
            return []
        if self.value == ".":
            return [self] + self.nodes[0].get_followpos_changer() + self.nodes[1].get_followpos_changer()
        elif self.value == "*":
            return [self] + self.nodes[0].get_followpos_changer()
        elif self.value == "|":
            return [] + self.nodes[0].get_followpos_changer() + self.nodes[1].get_followpos_changer()
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
        if (len(ps) == 1 or (len(ps) == 3 and ps[1] == "-")):
            return Node(ps)

        if (len(ps) == 2 and ps[0] == "\\"):
            return Node(ps[1])

        cur_level = 1
        levels = []
        aux = []

        rps = list(reversed(ps))

        is_counting = False
        ignore_char = False

        for i in range(len(rps)):
            if (i + 1 < len(rps) and rps[i+1] == "\\"):
                ignore_char = True

            if (rps[i] == "(" and not ignore_char):
                cur_level -= 1

            if rps[i] == "|" and cur_level == 1 and not ignore_char:
                return Node(
                    "|",
                    self.split_expression(''.join(reversed(rps[i+1:]))),
                    self.split_expression(''.join(reversed(rps[:i])))
                )
            elif rps[i] == "*" and cur_level == 1 and not ignore_char:
                aux.append("*")
                start_p = i
                is_counting = True
            elif rps[i] in ")" and cur_level == 1 and not ignore_char:
                aux.append(rps[i])
                if not is_counting:
                    start_p = i
            elif rps[i] in "(" and cur_level == 1 and not ignore_char:
                aux.append(rps[i])
                levels[start_p] = i
                is_counting = False
            elif rps[i] in "-" and i >= 1 and i <= len(rps) - 2 and cur_level == 1 and rps[i-1] not in "(|)*" and rps[i+1] not in "(|)*" and not ignore_char:
                aux.append(rps[i])
            elif is_counting:
                levels[start_p] = i
                is_counting = False
                aux.append(0)
            elif ignore_char:
                aux.append(-1)
            else:
                aux.append(0)

            levels.append(cur_level if cur_level == 1 else 0)

            if (rps[i] == ")" and not ignore_char):
                cur_level += 1

            ignore_char = False

        zipped = list(zip(aux, levels))

        items = []

        end = 0

        if (zipped[0] == (0, 1)):
            if (zipped[1] == (1, "-")):
                items.insert(0, ''.join(reversed(rps[:3])))
                end += 2
            else:
                items.insert(0, rps[0])
                end += 1
        elif (zipped[0][0] == ")"):
            end = zipped[0][1] + 1
            items.insert(0, ''.join(reversed(rps[:end])))
        elif (zipped[0][0] == "*"):
            end = zipped[0][1] + 1
            items.insert(0, ''.join(reversed(rps[:end])))
        elif (zipped[0][0] == -1):
            end += 2
            items.insert(0, ''.join(reversed(rps[:end])))

        if end >= len(rps):
            if zipped[0][0] == ")":
                return self.split_expression(items[0][1:-1])
            elif zipped[0][0] == "*":
                return Node("*", self.split_expression(items[0][:-1]))

        if (zipped[end][0] == ")"):
            new_end = zipped[end][1] + 1
            if (new_end >= len(zipped)):
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
