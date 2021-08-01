from os import forkpty
from operations import *
from AF import *
from ER import *

def start_lexical_analyzer(file_path, er_afd, ign_afd):

    file = open(file_path, 'r')
    data = file.read().replace('\n', '')
    file.close()

    symbol_table = []
    lexeme_begin = 0 
    forward = 0
    i = 0

    count = 0
    while i < len(data):
        er_afd.current_state = er_afd.S
        lexeme = ""

        while ((data[forward]) == ' '):
            forward = forward + 1

        if er_afd.current_state is not None:

            er_afd.step(data[forward])
            lexeme_begin = forward
            lexeme_id = er_afd.current_state.regex_final_id
            print(lexeme_id)
            while (er_afd.current_state.regex_final_id == lexeme_id) and (data[forward] != ' '):
                er_afd.step(data[forward])
                forward = forward + 1

            if er_afd.current_state in er_afd.F:
                lexeme = data[lexeme_begin:forward]
                print("Lexema: "+lexeme+" ",er_afd.current_state.regex_final_id)
                symbol_table.append((lexeme, er_afd.current_state.regex_final_id))


                i = forward

    print(symbol_table)
