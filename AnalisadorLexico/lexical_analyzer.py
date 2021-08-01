from Operations import *
from AF import *
from ER import *


def start_lexical_analyzer(file_path, afd):

    file = open(file_path, 'r')
    data = file.read().replace('\n', '')
    file.close()

    symbol_table = []
    lexeme_begin = 0
    forward = 0
    i = 0

    count = 0

    add_symbol = False
    last_regex = None
    while i < len(data):
        [state, regex_id, success] = afd.test_input(
            data[lexeme_begin:i+1])

        if success:
            i += 1
            if regex_id[0] != '-':
                last_regex = regex_id[0]
                add_symbol = True
            else:
                lexeme_begin = i
        else:
            if add_symbol:
                symbol_table.append((data[lexeme_begin:i], last_regex))
                add_symbol = False
                lexeme_begin = i
            elif state == "error state":
                raise Exception(f"Erro na posição {i}")
            else:
                i += 1

    print(symbol_table)
