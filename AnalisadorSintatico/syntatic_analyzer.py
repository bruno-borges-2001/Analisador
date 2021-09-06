
def clr_1(grammar, sentence):

    table = grammar.get_LR_canonic_data()
    action_table = table[0]
    goto_table = table[1]
    stack = []

    stack.append("$")
    stack.append(0)
    lookahead = sentence[0]
    index = 0

    while True:
        last = stack[-1]

        print(stack)
        if (last, lookahead) in action_table:
            action = action_table[(last, lookahead)]

            if ('accept' in action):
                return True

            elif ('shift' in action):

                stack.append(lookahead)
                index += 1
                lookahead = sentence[index]
                stack.append(action[1])

            elif ('reduce' in action):

                for x in len(action[2]) * 2:
                    print('Pop')
                    stack.pop()
                old_last = stack[-1]
                last = stack.append(action[1])
                goto = goto_table[(old_last, last)]
                stack.append(goto[1])
        else:
            break
    
    return False
