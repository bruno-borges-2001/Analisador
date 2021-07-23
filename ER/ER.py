from Structures import ERTree


def group_char(string):
    pass


class ER:

    def __init__(self, regex):
        self.regex = regex

    def get_tree(self):
        tree = ERTree()
        tree.create_tree(self.regex)
        tree.pretty_print()
        leafs = tree.get_leafs()
        count = 0
        for l in leafs:
            count += 1
            l.nid = count
        nodes = tree.flat_tree()
        print(list(map(lambda x: x.value, nodes)))
