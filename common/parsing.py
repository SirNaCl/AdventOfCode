from re import findall


def uints(line: str) -> list[int]:
    return list(map(int, findall(r"\d+", line)))


def ints(line: str) -> list[int]:
    return list(map(int, findall(r"-?\d+", line)))
