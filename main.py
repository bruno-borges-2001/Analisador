from AF import *
from Grammar import *

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

# p = State("{p}")
# q = State("{q}")
# r = State("{r}")

# K = [p, q, r]
# E = [EPSILON, "a", "b", "c"]

# create_condition = make_create_condition(E)
# T = {
#     p.id: create_condition([None, p, q, r]),
#     q.id: create_condition([p, q, r, None]),
#     r.id: create_condition([q, r, None, p])
# }

# S = p
# F = [r]

# afnd = AFND(K, E, T, S, F)
# afnd.print_transition_table()

# afd = afnd.determinize()
# afd.print_transition_table()

# S = State("S")
# A = State("A")
# B = State("B")
# C = State("C")
# D = State("D")
# X = State("X")

# K = [S, A, B, C, D, X]
# E = ["0", "1"]

# create_condition = make_create_condition(E)
# T = {
#     S.id: create_condition([[S, X], A]),
#     A.id: create_condition([B, C]),
#     B.id: create_condition([D, [S, X]]),
#     C.id: create_condition([A, B]),
#     D.id: create_condition([C, D]),
#     X.id: create_condition([None, None]),
# }

# S = S
# F = [X]

# afnd = AFND(K, E, T, S, F)
# afnd.print_transition_table()

# afd = afnd.determinize()
# afd.print_transition_table()

g1 = Grammar(*ParseGrammar("tests/teste.txt").get_params(), "m1")
r1 = g1.get_strings_from_generation_list(g1.generate(1000, False))

g2 = Grammar(*ParseGrammar("tests/teste2.txt").get_params(), "m2")
r2 = g2.get_strings_from_generation_list(g2.generate(1000, False))

g3 = Grammar(*ParseGrammar("tests/teste3.txt").get_params(), "m3")
r3 = g3.get_strings_from_generation_list(g3.generate(10000, False))

print(len(r3))

# r = []
# for i in r1:
#     if i not in r2 and i in r3:
#         r.append(i)

a = list(range(0, 30, 3))
b = list(range(0, 30, 3))

for i in r3:
    count = [0, 0]
    for c in i:
        count[int(c) - 1] += 1

    d = count[0] + 2 * count[1]
    if (d in b):
        b.remove(d)

    if (d not in a):
        print(i, count, d)

print(b)
