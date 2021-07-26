from AF import *


def union(AF1, AF2):
    new_initial_state_name = "us"

    while new_initial_state_name in AF1.states or new_initial_state_name in AF2.states:
        new_initial_state_name += "-"

    new_initial_state = State(new_initial_state_name)

    K = [new_initial_state] + AF1.states + AF2.states

    E = list(set([EPSILON] + AF1.E + AF2.E))
    E.sort()

    # acho que AF1.E e AF2.E deve ser igual
    # if AF1.E != AF2.E:
    #     raise Exception("Automatos devem aceitar as mesmas entradas para união")

    create_condition = make_create_condition(E)
    T = {
        new_initial_state.id: create_condition(
            [AF1.S, AF2.S] + [None] * (len(E) - 2)
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
