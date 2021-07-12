from AF import *

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

print(afnd.get_string_states_from_list(afnd.epsilon_fecho(p)))
print(afnd.get_string_states_from_list(afnd.epsilon_fecho(q)))
print(afnd.get_string_states_from_list(afnd.epsilon_fecho(r)))

afd = afnd.determinize()
afd.print_transition_table()
