from .__init__ import EPSILON

from .utils import *
from copy import deepcopy


class State:

    def __init__(self, name, derived_states=None):
        self.id = str(id(self))
        self.name = name
        self.derived_states = derived_states

    def __eq__(self, other):
        return id(self) == id(other) or self.name == other.name

    def __lt__(self, other):
        return self.name < other.name


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


class AFND(AFD):

    def __init__(self, K, E, T, S, F):
        super().__init__(K, E, T, S, F)

    def epsilon_fecho(self, k):
        if EPSILON not in self.E:
            return [k.id]

        p = [k]
        c = set([k.id])

        while len(p) > 0:
            s = p.pop()
            next_state = self.T[s.id](EPSILON)
            if (type(next_state) == list):
                for r in next_state:
                    if r.id not in c:
                        p.append(r)
                        c.add(r.id)
            elif (type(next_state) == State):
                if next_state.id not in c:
                    p.append(next_state)
                    c.add(next_state.id)

        c = list(c)
        c.sort()
        return c

    def test_input(self, input_string):
        self.current_state = list(self.epsilon_fecho(self.S))
        for i in input_string:
            aux = []
            while len(self.current_state) > 0:
                state = self.current_state.pop(0)
                state = self.K[state]
                aux += self.step(state, i)
            self.current_state = list(set(self.current_state + aux))
            if len(self.current_state) == 0:
                return ("error state", False)

        self.current_state = list(map(lambda x: self.K[x], self.current_state))

        accept = False
        for state in self.current_state:
            if state in self.F:
                accept = True

        return (
            list(map(lambda x: x.name, self.current_state)),
            accept
        )

    def step(self, s, e):
        aux = []
        next_states = self.T[s.id](e)
        if (type(next_states) == list):
            for state in next_states:
                aux += self.epsilon_fecho(state)
        elif (type(next_states) == State):
            aux += self.epsilon_fecho(next_states)

        return aux

    def get_string_states_from_list(self, li):
        return ','.join(list(map(lambda x: self.K[x].name, li)))

    def get_list_states_by_ids(self, li):
        return list(map(lambda x: self.K[x], li))

    def get_list_ids_by_states(self, li):
        return list(map(lambda x: x.id, li))

    def determinize(self):
        K = []
        E = deepcopy(self.E)
        E.remove(EPSILON)

        create_condition = make_create_condition(E)
        T = {}

        S_states = self.epsilon_fecho(self.S)
        S_name = self.get_string_states_from_list(S_states)
        S_derived_states = self.get_list_states_by_ids(S_states)
        S = State(S_name, S_derived_states)
        K.append(S)

        F = []

        test_states = [S]
        while len(test_states) > 0:
            current_state = test_states.pop(0)
            current_state_transition = []
            for e in E:
                next_states = []
                for cs in current_state.derived_states:
                    for i in self.step(cs, e):
                        next_states += self.epsilon_fecho(self.K[i])

                next_states = list(set(next_states))
                next_states.sort()
                new_state = State(
                    self.get_string_states_from_list(next_states),
                    self.get_list_states_by_ids(next_states)
                )

                if new_state not in K:
                    K.append(new_state)
                    test_states.append(new_state)
                    current_state_transition.append(new_state)
                    if find_any_el_from_list(new_state.derived_states, self.F):
                        F.append(new_state)
                else:
                    current_state_transition.append(
                        next(i for i in K if i == new_state)
                    )
            T[current_state.id] = create_condition(current_state_transition)

        return AFD(K, E, T, S, F)