def preprocess(filename):
    txt = open(filename, "r")
    UnitList = []
    for line in txt:
        Separate = line.split(";")
        Separate[1] = Separate[1].split()[0]
        UnitList.append(Separate)
    return UnitList
