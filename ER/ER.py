from DEFINITIONS import *

from Structures import ERTree
from AF import make_create_condition, AFD, AFND, State


class ER:

    def __init__(self, erid, regex):
        self.id = erid
        self.regex = regex

    def parse_generic(self, ps):
        try:
            i = ps.index("-")
            replace_string = ""
            while True:
                if ps[i-1] in DIG and ps[i+1] in DIG and DIG.index(ps[i-1]) < DIG.index(ps[i+1]):
                    replace_string = UNION.join(
                        DIG[DIG.index(ps[i-1]):DIG.index(ps[i+1])+1])
                else:
                    raise Exception("Erro de formação")

                ps = ps.replace(ps[i-1:i+2], replace_string)

                i = ps.index("-")
        except ValueError:
            self.regex = ps

    def get_entries(self):
        E = []
        ignore_next = False
        ignore_chars = ["(", UNION, CLOSURE, ")", ONEORNONE]
        add_next = False
        for i in range(len(self.regex)):
            if add_next:
                add_next = False
                E.append(self.regex[i])
            if ignore_next:
                ignore_next = False
                continue
            if self.regex[i] == "\\":
                add_next = True
                continue
            if self.regex[i] not in ignore_chars:
                if self.regex[i] == "-" and i-1 >= 0 and i+1 < len(self.regex) and self.regex[i-1] not in ignore_chars and self.regex[i+1] not in ignore_chars:
                    ignore_next = True
                    E.pop()
                    E.append(self.regex[i-1:i+2])
                else:
                    E.append(self.regex[i])
        return list(set(E))

    def get_entries_from_group(self, group):
        [start, end] = list(map(lambda x: DIG.index(x), group.split("-")))
        E = []
        for c in range(len(DIG)):
            if start > end:
                if c >= start or c <= end:
                    E.append(DIG[c])
            else:
                if c >= start and c <= end:
                    E.append(DIG[c])
        return E

    def check_entry_in_group(self, e, group):
        [start, end] = list(map(lambda x: DIG.index(x), group.split("-")))
        E = self.get_entries_from_group(group)
        return e in E

    def get_afd(self, debug=False):
        # create tree from regex
        tree = ERTree()
        [leaves, fp_nodes] = tree.create_tree(self.regex)

        if debug:
            tree.pretty_print()

        # get followpos
        followpos = dict((str(el.nid), []) for el in leaves)

        for node in fp_nodes:
            if node.value == ".":
                for i in node.nodes[0].lastpos():
                    followpos[str(i.nid)] += node.nodes[1].firstpos()
                    followpos[str(i.nid)] = list(set(followpos[str(i.nid)]))
            elif node.value == "*":
                for i in node.lastpos():
                    followpos[str(i.nid)] += node.firstpos()
                    followpos[str(i.nid)] = list(set(followpos[str(i.nid)]))

        for k, v in followpos.items():
            v.sort()
            if debug:
                print(k, list(map(lambda x: x.nid, v)))

        # start the afd creation
        K = []
        E = self.get_entries()
        E.sort()

        create_condition = make_create_condition(E)

        S_firstpos = list(map(lambda x: x.nid, tree.root.firstpos()))
        S_firstpos.sort()
        S_name = ','.join(map(str, S_firstpos))

        S = State(S_name)
        K.append(S)

        Dstates = {}
        Dstates[S_name] = False

        T = {}

        F = []

        # get states and transitions
        while False in Dstates.values():
            cur_state_name = [k for k, v in Dstates.items() if v == False][0]
            cur_state = [k for k in K if k == cur_state_name][0]
            cur_state_entries = cur_state_name.split(',')
            cur_state_transitions = []
            Dstates[cur_state_name] = True
            for e in E:
                U_list = []
                for cse in cur_state_entries:
                    if len([l for l in leaves if cse == str(l.nid) and l.value == e]) > 0:
                        U_list += followpos[cse]
                if (len(U_list) == 0):
                    cur_state_transitions.append(None)
                    continue
                U_list = list(set(U_list))
                U_list.sort()
                U_name = ','.join(map(lambda x: str(x.nid), U_list))
                U = None
                if U_name not in Dstates.keys():
                    Dstates[U_name] = False
                    U = State(U_name)
                    K.append(U)
                else:
                    U = [k for k in K if k == U_name][0]

                if str(leaves[-1].nid) in U_name and U not in F:
                    F.append(U)

                cur_state_transitions.append(U)

            T[cur_state.id] = create_condition(cur_state_transitions)

        new_E = []
        for e in E:
            if len(e) > 1 and "-" in e:
                new_E += self.get_entries_from_group(e)
            else:
                new_E += e
        new_E = list(set(new_E))
        new_E.sort()

        # parse generic groups (u.e. a-z)
        create_condition = make_create_condition(new_E)

        new_T = {}
        for k in K:
            transitions = []
            for e in new_E:
                next_states = []
                if e in E:
                    next_states.append(T[k.id](e))
                groups = [g for g in E if len(
                    g) > 1 and "-" in g and self.check_entry_in_group(e, g)]
                for g in groups:
                    next_states.append(T[k.id](g))

                next_states = [ns for ns in next_states if ns is not None]

                if len(next_states) == 0:
                    next_states = None

                transitions.append(next_states)

            new_T[k.id] = create_condition(transitions)

        for f in F:
            f.regex_final_id = [self.id]

        # parsing generic groups generate an AFND, so determinizing is needed
        afd = AFND(K, new_E, new_T, S, F).determinize()

        if debug:
            afd.print_transition_table()

        return afd
