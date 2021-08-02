from Operations import *
from AF import *
from ER import *


# def insert_token_file(filename):
#     token_file = open(filename)

#     token_er_dict = {}

#     token_er_dict["reserved_words"] = None

#     reserved_words = {}

#     ignore_er = []

#     for line in token_file.readlines():
#         line = line.replace("\n", "")
#         if len(line) == 0:
#             continue

#         if line[0] == "#":
#             continue

#         if line[0] == "\"":
#             ignore_er.append(ER("-", line[1:-1]).get_afd())
#             continue

#         [fp, sp] = line.split("=", 1)

#         if ":" in sp and sp[sp.index(":") - 1] != "\\":
#             [pattern, er_string] = sp.split(":", 1)

#             er_string = er_string[1:-1]

#             if pattern in token_er_dict.keys() and token_er_dict[pattern].test_input(er_string)[-1]:
#                 reserved_words[fp] = er_string

#         else:
#             token_er_dict[fp] = ER(fp, sp[1:-1]).get_afd()

#     token_file.close()

#     token_er_dict["reserved_words"] = ER(
#         "RW", '|'.join(reserved_words.values())).get_afd()

#     ERs = list(token_er_dict.values())

#     if len(ERs) == 0:
#         exit()
#     elif len(ERs) == 1:
#         afnd = ERs[0]
#     elif len(ERs) >= 2:
#         afnd = union(ERs[0], ERs[1])
#         for er in ERs[2:]:
#             afnd = union(afnd, er)

#     er_afd = afnd.determinize()

#     ig_afnd = None

#     if len(ignore_er) == 1:
#         ig_afnd = ignore_er[0]
#     elif len(ignore_er) >= 2:
#         ig_afnd = union(ignore_er[0], ignore_er[1])
#         for i in ignore_er[2:]:
#             ig_afnd = union(ig_afnd, i)

#     ignored_afd = ig_afnd.determinize()

#     afd = union(er_afd, ignored_afd).determinize("S")
#     afd.print_transition_table("debug/AFD.txt")

#     return afd


def insert_token(file):
    token_er_dict = {}

    token_er_dict["reserved_words"] = None

    reserved_words = {}

    ignore_er = []

    for line in file.readlines():
        line = line.replace("\n", "")
        if len(line) == 0:
            continue

        if line[0] == "#":
            continue

        if line[0] == "\"":
            ignore_er.append(ER("-", line[1:-1]).get_afd())
            continue

        [fp, sp] = line.split("=", 1)

        if ":" in sp and sp[sp.index(":") - 1] != "\\":
            [pattern, er_string] = sp.split(":", 1)

            er_string = er_string[1:-1]

            if pattern in token_er_dict.keys() and token_er_dict[pattern].test_input(er_string)[-1]:
                reserved_words[fp] = er_string

        else:
            token_er_dict[fp] = ER(fp, sp[1:-1]).get_afd()

    file.close()

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

    er_afd = afnd.determinize()

    ig_afnd = None

    if len(ignore_er) == 1:
        ig_afnd = ignore_er[0]
    elif len(ignore_er) >= 2:
        ig_afnd = union(ignore_er[0], ignore_er[1])
        for i in ignore_er[2:]:
            ig_afnd = union(ig_afnd, i)

    ignored_afd = ig_afnd.determinize()

    afd = union(er_afd, ignored_afd).determinize("S")
    afd.print_transition_table("debug/AFD.txt")

    return afd


# def start_lexical_analyzer(file_path, afd):

#     file = open(file_path, 'r')
#     data = file.read().replace('\n', '')
#     file.close()

#     symbol_table = []
#     lexeme_begin = 0
#     forward = 0
#     i = 0

#     count = 0

#     add_symbol = False
#     last_regex = None
#     while i < len(data):
#         [state, regex_id, success] = afd.test_input(
#             data[lexeme_begin:i+1])

#         if success:
#             i += 1
#             if regex_id[0] != '-':
#                 last_regex = regex_id[0]
#                 add_symbol = True
#             else:
#                 lexeme_begin = i
#         else:
#             if add_symbol:
#                 symbol_table.append((data[lexeme_begin:i], last_regex))
#                 add_symbol = False
#                 lexeme_begin = i
#             elif state == "error state":
#                 print(f"Erro na posição {i}")
#                 break
#             else:
#                 i += 1

#     row_format = "{:>20}" * 2

#     print(row_format.format("Lexema", "Token"))

#     for i in symbol_table:
#         print(row_format.format(*i))


def sort_by_priority(li):
    new_li = []
    for i in reversed(li):
        if i == "RW":
            new_li.insert(0, i)
        else:
            new_li.append(i)
    return new_li


def get_char_coords(text, i):
    row = 1
    column = 0
    count = 0
    while count != i:
        if text[count] == "\n":
            count += 1
            row += 1
            column = 0
        else:
            count += 1
            column += 1
    return (row, column)


def start_lexical_analyzer(file, afd, set_error=None):

    # no_parsed_data = file.read()
    # data = no_parsed_data.replace("\n", " ")
    data = file.readlines()
    file.close()
    symbol_table = []
    count = 0

    for l in data:
        line = l.replace("\n", " ")
        add_symbol = False
        last_regex = None
        i = 0
        lexeme_begin = 0

        while i < len(line):
            [state, regex_id, success] = afd.test_input(
                line[lexeme_begin:i+1])

            if success:
                i += 1
                count += 1
                last_regex = sort_by_priority(regex_id)[0]
                add_symbol = True
            else:
                if add_symbol:
                    add_symbol = False
                    if last_regex != "-":
                        symbol_table.append((line[lexeme_begin:i], last_regex))
                    last_regex = None
                    lexeme_begin = i
                elif state == "error state":
                    if set_error is not None:
                        set_error(get_char_coords(''.join(data), count))
                    print(f"Erro na posição {count}")
                    i += 1
                    count += 1
                    lexeme_begin = i
                else:
                    i += 1
                    count += 1

        if last_regex is not None and last_regex != "-":
            symbol_table.append((line[lexeme_begin:i], last_regex))

    return symbol_table
