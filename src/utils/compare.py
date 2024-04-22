from thefuzz import fuzz


# TODO better name
# returns true if the needle is present in at least one, but not all of haystack
def occurrences(needle: str, haystack: list[str]) -> bool:
    occurrences = len([x for x in haystack if needle in x])
    return occurrences > 0 and occurrences < len(haystack)


# TODO better name
# Returns true for things like "Track 1 (2007 Remaster)" / "Track 2 (2007 Remaster)"
def diffTitleSameEnding(a: str, b: str) -> bool:
    aParts = a.split(' ')
    bParts = b.split(' ')
    # aParts.reverse()
    # bParts.reverse()

    if len(aParts) < 2 or len(bParts) < 2:
        return False

    for index, part in enumerate(aParts):
        subA = aParts[index:]

        if aParts[index] not in bParts:
            continue

        subB = bParts[bParts.index(aParts[index]):]

        if subA == subB:
            return True

    return False


# TODO - as expected, this ignores some stuff that shouldn't be ignored; maybe look specifically for "pt." etc
# TODO - better Name, clean up code
# Returns true for things like "TRACKNAME pt. 1" / "TRACKNAME pt. 2"
def sameTitleDiffEnding(a: str, b: str) -> bool:
    aParts = a.split(' ')
    bParts = b.split(' ')

    if len(aParts) < 2 or len(bParts) < 2:
        # print('here', len(aParts), len(bParts))
        return True

    index = 1
    while index <= min(len(aParts), len(bParts)):
        subA = aParts[index:]
        subB = bParts[index:]
        preA = aParts[:index]
        preB = bParts[:index]

        # print(subA, subB, preA, preB)
        if subA != subB and preA == preB:
            return True
        index += 1

    return False


def compare(_a: str, _b: str, log=False) -> bool:
    THRESHOLD = 80
    a = _a.lower()
    b = _b.lower()
    haystack = [a, b]

    if a == b:
        return True

    if occurrences('remix', haystack):
        return False

    if diffTitleSameEnding(a, b):
        return False

    if sameTitleDiffEnding(a, b):
        return False

    ratio = fuzz.ratio(a, b)
    return ratio > THRESHOLD
