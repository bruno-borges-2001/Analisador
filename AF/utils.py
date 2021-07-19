
def find_any_el_from_list(search_list, find_list):
    for i in search_list:
        if i in find_list:
            return True

    return False


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
