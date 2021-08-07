from DEFINITIONS import EPSILON
from .utils import *
from .State import *

from copy import deepcopy


class AFD:

    def __init__(self, K, E, T, S, F):
        self.states = K
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
            if State_Id(state.id) not in K:
                raise Exception("One or more final states are not in K")

    def test_input(self, input_string):
        self.current_state = self.S
        for i in input_string:
            self.step(i)
            if self.current_state is None:
                return ("error state", None, False)

        return (self.current_state.name, self.current_state.regex_final_id, self.current_state in self.F)

    def step(self, e):
        self.current_state = self.T[self.current_state.id](e)

    def print_transition_table(self, filename=None):
        row_format = "{:>25}" * (len(self.E) + 2)
        file = None
        if filename is not None:
            file = open(filename, "w")

        if file is not None:
            file.write(row_format.format("", "", *self.E) + "\n")
        else:
            print(row_format.format("", "", *self.E))

        for state_id, transitions in self.T.items():
            extra = ""
            state = self.K[state_id]
            sstate = "* " if state in self.F else ""
            sstate += "-> " if state == self.S else ""
            sstate += state.name
            if state in self.F and len(state.regex_final_id) > 0:
                extra = ','.join(state.regex_final_id)
            n_states = list(
                map(
                    lambda i: list(map(lambda x: x.name, i))
                    if type(i) == list else i.name if type(i) != type(None) else "-",
                    map(transitions, self.E)
                )
            )

            if file is not None:
                file.write(row_format.format(
                    extra, sstate, *map(str, n_states)) + "\n")
            else:
                print(row_format.format(extra, sstate, *map(str, n_states)))

        if file is not None:
            file.close()


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
            list(map(lambda x: (x.name, x.regex_final_id), self.current_state)),
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
        states = list(map(lambda x: self.K[x].name, li))
        return ','.join(states)

    def get_list_states_by_ids(self, li):
        return list(map(lambda x: self.K[x], li))

    def get_list_ids_by_states(self, li):
        return list(map(lambda x: x.id, li))

    def determinize(self, start_state_name=None):
        K = []
        E = deepcopy(self.E)
        if EPSILON in E:
            E.remove(EPSILON)

        create_condition = make_create_condition(E)
        T = {}

        # creating first state
        S_states = self.epsilon_fecho(self.S)
        S_name = self.get_string_states_from_list(S_states) if start_state_name is None \
            else start_state_name
        S_derived_states = self.get_list_states_by_ids(S_states)
        S = State(S_name, S_derived_states)
        K.append(S)

        F = [S] if find_any_el_from_list(S.derived_states, self.F) else []

        if len(F) > 0:
            for s in S.derived_states:
                if s in self.F:
                    S.regex_final_id += s.regex_final_id

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

                if len(next_states) == 0:
                    current_state_transition.append(None)
                    continue

                new_state = State(
                    self.get_string_states_from_list(next_states),
                    self.get_list_states_by_ids(next_states)
                )

                for s in new_state.derived_states:
                    if s in self.F:
                        new_state.regex_final_id += s.regex_final_id

                if new_state.name not in K:
                    K.append(new_state)
                    test_states.append(new_state)
                    current_state_transition.append(new_state)
                    if find_any_el_from_list(new_state.derived_states, self.F):
                        F.append(new_state)
                else:
                    current_state_transition.append(
                        next(i for i in K if new_state == i.name)
                    )
            T[current_state.id] = create_condition(current_state_transition)

        return AFD(K, E, T, S, F)
