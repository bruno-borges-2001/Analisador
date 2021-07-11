EPSILON = "*epsilon*"


class State:

    def __init__(self, name):
        self.id = str(id(self))
        self.name = name

    def __eq__(self, other):
        return id(self) == id(other)


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
        for state_id, transitions in T.items():
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
            return [k]

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

        return list(c)

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


def make_create_condition(E):
    def create_condition(K):
        if len(K) != len(E):
            raise Exception("K must have the same length as E")
        # transitions dict(key: entrada, value: prox_estado)
        transitions = dict(zip(E, K))

        def condition(e):
            return transitions[str(e)] if e in E else None

        return condition
    return create_condition


# q0 = State("{p}")
# q1 = State("{p,q}")
# q2 = State("{p,r}")
# q3 = State("{p,q,r}")
# q4 = State("{p,q,s}")
# q5 = State("{p,r,s}")
# q6 = State("{p,q,r,s}")
# q7 = State("{p,s}")
# K = [q0, q1, q2, q3, q4, q5, q6, q7]

# E = ["0", "1"]

# create_condition = make_create_condition(E)
# T = {
#     q0.id: create_condition([q1, q0]),
#     q1.id: create_condition([q3, q2]),
#     q2.id: create_condition([q4, q0]),
#     q3.id: create_condition([q6, q2]),
#     q4.id: create_condition([q6, q5]),
#     q5.id: create_condition([q4, q7]),
#     q6.id: create_condition([q6, q5]),
#     q7.id: create_condition([q4, q7])
# }
# S = q0
# F = [q4, q5, q6, q7]

# af = AFD(K, E, T, S, F)
# af.print_transition_table()
# print(af.test_input("00010010010101"))

p = State("{p}")
q = State("{q}")
r = State("{r}")

K = [p, q, r]
E = [EPSILON, "a", "b", "c"]

create_condition = make_create_condition(E)
T = {
    p.id: create_condition([None, p, q, r]),
    q.id: create_condition([p, q, r, None]),
    r.id: create_condition([q, r, None, p])
}

S = p
F = [r]

afnd = AFND(K, E, T, S, F)
afnd.print_transition_table()
print(afnd.test_input("ba"))
