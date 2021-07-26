class State:

    def __init__(self, name, derived_states=None):
        self.id = str(id(self))
        self.name = name
        self.derived_states = derived_states

    def __eq__(self, other):
        return other is not None and (id(self) == id(other) or self.name == other.name)

    def __lt__(self, other):
        return self.name < other.name
