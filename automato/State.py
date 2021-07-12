class State:

    def __init__(self, name):
        self.id = str(id(self))
        self.name = name

    def __eq__(self, other):
        return id(self) == id(other)