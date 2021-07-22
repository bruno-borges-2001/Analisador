from Structures import ERTree


def group_char(string):
    pass


class ER:

    def __init__(self, regex):
        self.regex = regex

    def get_tree(self):
        tree = ERTree()
        tree.create_tree(self.regex)
        tree.pretty_print(tree.root)
