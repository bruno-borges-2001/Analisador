from Structures import Set


class Grammar:
    N: Set = None
    T: Set = None
    P: dict = {}
    S: str = None

    def __init__(self, N: Set = None, T: Set = None, P: dict = None, S: str = None, filename=None):
        if filename:
            self.read_file(filename)
        else:
            self.N = N
            self.T = T
            self.P = P
            self.S = S

        self.check_grammar()
        # self.remove_left_recursion()

        self.FIRST = {}
        self.FOLLOW = {}

        self.get_first()
        self.get_follow()

    def read_file(self, filename):
        N = Set()
        T = Set()
        P = {}
        S = None

        file = open(filename, 'r+')
        lines = file.readlines()
        file.close()

        for line in lines:
            line = line.replace("\n", "")
            nt, t = self.parse_string(line)

            for i in t:
                T.append(i)

            N.append(nt)

            if S is None:
                S = nt

            T = T + Set(t)

            if nt in P:
                P[nt].append(t)
            else:
                P[nt] = Set([t])

        T = T - N - Set(["&"])

        self.N = N
        self.T = T
        self.P = P
        self.S = S

    def parse_string(self, string):
        non_terminal, _, *production = string.split(' ')

        if len(production) == 0:
            production = ["&"]

        return (non_terminal, production)

    def check_grammar(self):
        return len(self.T.intersection(self.N)) == 0 and self.S in self.N

    def belongs(self, el, production):
        for i in production:
            if el in i:
                return True
        return False

    def remove_direct_left_recursion(self, A, production):
        alpha = []
        beta = []
        for i in production.values:
            if i[0] == A:
                alpha.append(i[1:])
            else:
                beta.append(i)

        if len(alpha) == 0:
            return {A: production}
        new_A = A + "'"

        new_p = {
            A: Set([[*bn, new_A] for bn in beta]),
            new_A: Set([[*an, new_A] for an in alpha] + [["&"]])
        }

        return new_p

    def remove_left_recursion(self):
        P = self.P.copy()
        nP = {}
        A = self.N.values
        for i in range(len(A)):
            nP[A[i]] = P[A[i]].copy()
            for j in range(i):
                for production in nP[A[i]].values:
                    if production[0] == A[j]:
                        nP[A[i]].remove(production)
                        alpha = production[1:]
                        for beta in nP[A[j]]:
                            if A[i] in nP:
                                nP[A[i]].append([*beta, *alpha])
                            else:
                                nP[A[i]] = Set([[*beta, *alpha]])
            nP.update(self.remove_direct_left_recursion(A[i], nP[A[i]]))
        self.N = Set(list(nP.keys()))
        self.P = nP

    def first(self, X):
        if X in self.T:
            return Set([X])
        elif X in self.N:
            FIRST = Set()
            keep_epsilon = False
            for Y in self.P[X]:
                if Y[0] in self.T:
                    FIRST.append(Y[0])
                elif Y[0] == "&":
                    FIRST.append(Y[0])
                    keep_epsilon = True
                else:
                    for i, y in enumerate(Y):
                        if y == X:
                            break
                        yi_first = self.first(y)
                        FIRST = FIRST + yi_first
                        if "&" in yi_first:
                            if i < len(Y) - 1 and not keep_epsilon:
                                FIRST.remove("&")
                            continue
                        else:
                            break
            return FIRST
        elif len(X) > 1:
            FIRST = Set()
            for x in X:
                if "&" in FIRST:
                    FIRST.remove("&")

                FIRST = FIRST + self.FIRST[x]

                if "&" not in FIRST:
                    break
            return FIRST
        else:
            return None

    def get_first(self):
        grammar_symbols = self.T + self.N
        for x in grammar_symbols:
            self.FIRST[x] = self.first(x)

    def unpack_productions(self):
        productions = []
        for A, P in self.P.items():
            for p in P:
                productions.append((A, p))
        return productions

    def get_follow(self):
        follow_dict = {}

        for x in Set([self.S]) + self.N:
            follow_dict[x] = Set()

        follow_dict[self.S].append("$")

        old_dict = follow_dict.copy()

        piter = self.unpack_productions()
        while True:

            for A, P in piter:
                for i, B in enumerate(P):
                    if B not in self.N:
                        continue

                    beta = P[i+1:]

                    if len(beta) > 0:
                        for b in beta:
                            follow_dict[B] = follow_dict[B] + self.FIRST[b]

                            if "&" in follow_dict[B]:
                                follow_dict[B].remove("&")
                            else:
                                break
                    else:
                        follow_dict[B] = follow_dict[B] + follow_dict[A]

            if follow_dict == old_dict:
                break

            old_dict = follow_dict.copy()

        self.FOLLOW = follow_dict

    def get_LR_canonic_data(self):
        new_S = self.S + "'"
        new_P = self.P
        new_P[new_S] = Set([[self.S]])

        nG = Grammar(N=self.N, T=self.T + Set(["$"]), P=new_P, S=new_S)

        C, fGOTO = self.items(nG)

        ACTION = {}
        GOTO = {}

        for i, I in enumerate(C):
            for A, p, b in I:
                idot = p.index(".")

                a = p[idot+1] if idot < len(p) - 1 else None
                Ij = fGOTO(I, a)

                # rule A
                if a in nG.T and a != b and Ij in C:
                    if (i, a) in ACTION:
                        raise Exception("Grammar is not LR(1)")
                    else:
                        ACTION[(i, a)] = ("shift", C.index(Ij))

                # rule B
                if a is None:
                    alpha = list(p[:idot])

                    if len(alpha) == 0:
                        alpha = ["&"]

                    if A != nG.S:
                        if (i, b) in ACTION:
                            raise Exception("Grammar is not LR(1)")
                        else:
                            ACTION[(i, b)] = ("reduce", A, alpha)

                # rule C
                if A == nG.S and p == ("S", ".") and b == "$":
                    ACTION[(i, "$")] = ("accept")

            for A in nG.N:
                Ij = fGOTO(I, A)
                if Ij in C:
                    j = C.index(Ij)
                    GOTO[(i, A)] = j

        return (ACTION, GOTO)

    def items(self, G):
        def CLOSURE(I):
            closure = Set(I)

            included = True

            while included:
                included = False

                for A, P, a in closure:
                    idot = P.index(".")

                    if idot == len(P) - 1:
                        continue

                    B = P[idot+1]
                    beta = P[idot+2:]

                    if B in G.P:
                        old_size = 0 + closure.size
                        for gama in G.P[B]:
                            if gama == ["&"]:
                                gama = []

                            first = G.first("".join(beta) + a)
                            for b in first:
                                if b in G.T:
                                    closure.append((B, (".", *gama), b))
                        if closure.size > old_size:
                            included = True

            return closure

        def GOTO(I, X):
            goto = Set()

            included = True

            for A, P, a in I:
                idot = P.index(".")

                if idot == len(P) - 1:
                    continue

                if P[idot+1] == X:
                    alpha = P[:idot]
                    beta = P[idot+2:]

                    new_value = (*alpha, X, ".", *beta)

                    goto.append((A, new_value, a))

            return CLOSURE(goto.values)

        C = Set()

        C.append(CLOSURE([(G.S, (".", *G.P[G.S].values[0]), "$")]))

        included = True
        while included:
            included = False

            for I in C.values:
                grammar_symbols = G.N + G.T
                for X in grammar_symbols.values:
                    goto = GOTO(I, X)
                    if goto.size > 0:
                        old_size = 0 + C.size
                        C = C + Set([goto])
                        if C.size > old_size:
                            included = True

        return (C, GOTO)
