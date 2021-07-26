from DEFINITIONS import *

from Structures import ERTree
from AF import make_create_condition, AFD, State


def group_char(string):
    pass


LC = "abcdefghijklmnopqrstuvwxyz"
UC = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
NUM = "0123456789"


class ER:

    def __init__(self, regex):
        self.regex = regex

    def parse_generic(self, ps):
        try:
            i = ps.index("-")
            replace_string = ""
            while True:
                if ps[i-1] in LC and ps[i+1] in LC and LC.index(ps[i-1]) < LC.index(ps[i+1]):
                    replace_string = UNION.join(
                        LC[LC.index(ps[i-1]):LC.index(ps[i+1])+1])
                elif ps[i-1] in UC and ps[i+1] in UC and UC.index(ps[i-1]) < UC.index(ps[i+1]):
                    replace_string = UNION.join(
                        UC[UC.index(ps[i-1]):UC.index(ps[i+1])+1])
                elif ps[i-1] in NUM and ps[i+1] in NUM and NUM.index(ps[i-1]) < NUM.index(ps[i+1]):
                    replace_string = UNION.join(
                        NUM[NUM.index(ps[i-1]):NUM.index(ps[i+1])+1])
                else:
                    raise Exception("Erro de formação")

                ps = ps.replace(ps[i-1:i+2], replace_string)

                i = ps.index("-")
        except ValueError:
            self.regex = ps

    def get_entries(self):
        E = []
        ignore_next = False
        ignore_chars = ["(", "|", "*", ")"]
        for i in range(len(self.regex)):
            if ignore_next:
                ignore_next = False
                continue
            if self.regex[i] not in ignore_chars:
                if self.regex[i] == "-" and i-1 >= 0 and i+1 < len(self.regex) and self.regex[i-1] not in ignore_chars and self.regex[i+1] not in ignore_chars:
                    ignore_next = True
                    E.pop()
                    E.append(self.regex[i-1:i+2])
                else:
                    E.append(self.regex[i])
        return list(set(E))

    def get_afd(self, debug=False):
        tree = ERTree()
        [leaves, fp_nodes] = tree.create_tree(self.regex)

        if debug:
            tree.pretty_print()

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

        while False in Dstates.values():
            cur_state_name = [k for k, v in Dstates.items() if v == False][0]
            cur_state = [k for k in K if k == State(cur_state_name)][0]
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
                    if str(leaves[-1].nid) in U_name:
                        F.append(U)
                else:
                    U = [k for k in K if k == State(U_name)][0]

                cur_state_transitions.append(U)

            T[cur_state.id] = create_condition(cur_state_transitions)

        afd = AFD(K, E, T, S, F)

        if debug:
            afd.print_transition_table()

        return afd
