from AF import *


def union(AF1, AF2):
    # creates the start state and avoids repeating names
    new_initial_state_name = "us"

    while new_initial_state_name in AF1.states or new_initial_state_name in AF2.states:
        new_initial_state_name += "-"

    new_initial_state = State(new_initial_state_name)

    # parse AF2 states to avoid repeating names
    for s in AF2.states:
        while True:
            if s.name in list(map(lambda x: x.name, AF1.states)):
                s.name = "-" + s.name
            else:
                break

    K = [new_initial_state] + AF1.states + AF2.states

    E = AF1.E + AF2.E
    # guarantees EPSILON on the start of the list
    if EPSILON in E:
        E.remove(EPSILON)
    E = list(set(E))
    E.sort()
    E = [EPSILON] + E

    create_condition = make_create_condition(E)
    T = {
        new_initial_state.id: create_condition(
            [[AF1.S, AF2.S]] + [None] * (len(E) - 1)
        )
    }

    # Adicionar transições de AF1 e AF2
    T.update(AF1.T)
    T.update(AF2.T)

    # Estado criado é o estado inicial
    S = new_initial_state

    # Estados finais são os estados finais de AF1 e AF2
    F = AF1.F + AF2.F

    return AFND(K, E, T, S, F)
