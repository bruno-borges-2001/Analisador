from .State import State

class AFD:

    def __init__(self, K, E, T, S, F):
        self.set_state_map(K)

        self.E = E
        self.T = T
        self.S = S
        self.F = F

        self.check()

        self.current_state = self.S

    def set_state_map(self, K):
        self.K = {}
        for i in K:
            self.K[i.id] = i

    def check(self):
        K = self.K.values()
        if self.S not in K:
            raise Exception("Initial state is not in K")

        for state in self.F:
            if state not in K:
                raise Exception("One or more final states are not in K")

    def test_input(self, input_string):
        self.current_state = self.S
        for i in input_string:
            self.step(i)
            if self.current_state is None:
                return ("error state", False)

        return (self.current_state.name, self.current_state in self.F)

    def step(self, e):
        self.current_state = self.T[self.current_state.id](e)

    def print_transition_table(self):
        row_format = "{:>15}" * (len(self.E) + 1)
        print(row_format.format("", *self.E))
        for state_id, transitions in self.T.items():
            state = self.K[state_id]
            state = "-> " + state.name if state == self.S else "* " + \
                state.name if state in self.F else state.name
            n_states = list(
                map(
                    lambda i: list(map(lambda x: x.name, i))
                    if type(i) == list else i.name if type(i) != type(None) else "-",
                    map(transitions, self.E)
                )
            )

            print(row_format.format(state, *map(str, n_states)))
