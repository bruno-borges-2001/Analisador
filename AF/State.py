class State_Id:
    def __init__(self, sid):
        self.id = sid


class State:

    def __init__(self, name, derived_states=None):
        self.id = str(id(self))
        self.name = name
        self.derived_states = derived_states

    def __eq__(self, other):
        if (type(other) == State_Id):
            return self.id == other.id
        if (type(other) == type("string")):
            return self.name == other
        return other is not None and (id(self) == id(other) or self.name == other.name)

    def __lt__(self, other):
        return self.name < other.name
