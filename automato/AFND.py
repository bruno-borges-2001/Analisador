from .State import State
from .AF import AFD





class AFND(AFD):
    EPSILON = "*epsilon*"
    
    def __init__(self, K, E, T, S, F):
        super().__init__(K, E, T, S, F)

    def epsilon_fecho(self, k):
        if AFND.EPSILON not in self.E:
            return [k]

        p = [k]
        c = set([k.id])

        while len(p) > 0:
            s = p.pop()
            next_state = self.T[s.id](AFND.EPSILON)
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