from operations import *
from AF import *
from ER import *
from AnalisadorLexico import *

token_file = open("debug/tokens.txt")

token_er_dict = {}

reserved_words = {}

ignore_er = []

ER("string", "\"(0-z| )*\"").get_afd().test_input("\"hello world\"")

for line in token_file.readlines():
    if "\n" in line:
        line = line[:-1]
    if len(line) == 0:
        continue

    if line[0] == "#":
        continue

    if line[0] == "\"":
        ignore_er.append(ER("-", line[1:-1]).get_afd())
        continue

    [fp, sp] = line.split("=", 1)

    if ":" in sp:
        [pattern, er_string] = sp.split(":", 1)

        er_string = er_string[1:-1]

        if pattern in token_er_dict.keys() and token_er_dict[pattern].test_input(er_string)[-1]:
            reserved_words[fp] = er_string

    else:
        token_er_dict[fp] = ER(fp, sp[1:-1]).get_afd()

token_file.close()

token_er_dict["reserved_words"] = ER(
    "RW", '|'.join(reserved_words.values())).get_afd()

ERs = list(token_er_dict.values())

if len(ERs) == 0:
    exit()
elif len(ERs) == 1:
    afnd = ERs[0]
elif len(ERs) >= 2:
    afnd = union(ERs[0], ERs[1])
    for er in ERs[2:]:
        afnd = union(afnd, er)


er_afd = afnd.determinize("S")
er_afd.print_transition_table("debug/AFD.txt")

ig_afnd = None

if len(ignore_er) == 1:
    ig_afnd = ignore_er[0]
elif len(ignore_er) >= 2:
    ig_afnd = union(ignore_er[0], ignore_er[1])
    for i in ignore_er:
        ig_afnd = union(ig_afnd, i)


ignored_afd = ig_afnd.determinize("I")
ignored_afd.print_transition_table("debug/IG_AFD.txt")

# TODO: Por algum motivo o operador ":" nao eh reconhecido pelo AFD.
# TODO: Eh possivel juntar o er_afd e ignored_afd em um unico AFD?
# Se for possivel, ficaria mais facil pois nao daria problema de NoneType
# TODO: Por algum motivo o operador "def" eh reconhecido como id

#print(er_afd.test_input(':'))
#print(er_afd.text_input('def'))
#print(er_afd.test_input('teste:'))
start_lexical_analyzer("debug/input.txt", er_afd, ignored_afd)

