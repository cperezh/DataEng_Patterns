def extract_movimientos():
    with open("./data/movements-15112025.csv", "r", encoding="UTF8") as f:
        # skip header
        f.readlines(4)

        for line in f.readlines():
            pass