


def build_file(name, data): 
    f = open (name, "w")
    from urllib.parse import unquote
    # data = data.replace("\\t", "  ")
    # data = data.replace("\\s", " ")
    # data = data.replace("PLUS", "+")
    data = unquote(data)
    print(data)
    lines = data.split("\\n")

    print(lines)

    with f as fl: 
        f.write(data)

    # with f as fl: 
    #     for line in lines: 
    #         f.write(line + "\n")

    f.close()