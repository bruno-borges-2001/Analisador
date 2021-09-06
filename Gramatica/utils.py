def format_action(action, P):
    if action is None:
        return "-"

    if action[0] == "shift":
        return f"s{action[1]}"
    elif action[0] == "reduce":
        prod = action[2]
        if len(prod) == 0:
            prod = ["&"]
        production = P.index((action[1], prod)) + 1
        return f"r{production}"
    elif action[0] == "accept":
        return "acc"


def pretty_print(C, ACTION, GOTO, N, T, P):
    P = P.unpack_productions()
    T.append("$")
    f = open("print.txt", "w+")
    header = [" ", "ACTION", "GOTO"]
    subheader = ["STATE", *T, *N]

    lengths = [
        len(subheader[0]),
        sum(map(lambda x: len(x) + 2, T)),
        sum(map(lambda x: len(x) + 2, N))
    ]

    lines = [subheader]
    for i in range(C.size):
        line = [i]

        for t in T:
            action = format_action(ACTION.get((i, t)), P)
            line.append(action)
            if len(action) + 2 > lengths[1]:
                lengths[1] = len(action) + 2

        for n in N:
            goto = GOTO.get((i, n))
            if goto:
                line.append(goto)
                if len(str(goto)) + 2 > lengths[2]:
                    lengths[2] = len(str(goto)) + 2
            else:
                line.append("-")

        lines.append(line)

    first_row_format = "{:^" + str(lengths[0]) + "} | "
    first_row_format += ("{:^" + str(lengths[1] * T.size) + "}") + " | "
    first_row_format += ("{:^" + str(lengths[2] * N.size) + "}")

    f.write(first_row_format.format(*header) + "\n")

    row_format = "{:^" + str(lengths[0]) + "} | "
    row_format += ("{:^" + str(lengths[1]) + "}") * T.size + " | "
    row_format += ("{:^" + str(lengths[2]) + "}") * N.size

    for line in lines:
        f.write(row_format.format(*line) + "\n")
