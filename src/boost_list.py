from math import sqrt

def uniq(l: list) -> list:
    """
    1.1
    Return a list removed form its duplicates
    """
    result = []
    i = 0

    while i != len(l):
        if result.count(l[i]) == 0:
            result.append(l[i])
        i += 1

    return result

def sort_uniq(l: list) -> list:
    """
    1.1
    Remove the duplicates in an sorted list
    """
    i = 1
    rst = [l[0]]

    while i != len(l):
        if l[i - 1] != l[i]:
            rst.append(l[i])
        i += 1

    return rst

def flatten(l: list) -> list:
    """
    1.2
    Flatten a multi dimensional list
    [[1, 2], [2, 4]], gives : [1, 2, 2, 4]
    """
    flat_list = []

    for el in l:
        if isinstance(el, list):
            flat_list.extend(flatten(el))
        else:
            flat_list.append(el)

    return flat_list

def successive_ints(l: list) -> list:
    """
    1.3
    Return a list containing the successive integers in the list given in argument
    """
    rst = []

    for i in range(len(l) - 1):
        if l[i] == l[i + 1] - 1:
            rst.append([l[i], l[i + 1]])

    return rst

def occurrences(l: list) -> dict:
    """
    1.4
    Return a dictionnary, containing the number of occurrences of an int in the
    list given in argument
    """
    d = dict()
    numbers = uniq(l)

    for el in l:
        d[el] = l.count(el)

    return d

def dice_combinations() -> dict:
    """
    1.5
    Returns the combinations of 2 dices. The key is the result, and
    the value is a 2D list of 2 lengthed list (2 dices)
    {1: [[1, 1]], 2:[[2, 1], [1, 2]], ...}
    """
    combinations = {n:[] for n in range(2, 13)}

    for i in range(1, 6 + 1):
        for j in range(1, 6 + 1):
            combinations[i + j].append([i, j])

    return combinations

def erathostenes_sieve(n: int) -> dict:
    """
    1.6
    Returns a dictionary containing prime numbers
    It is not recommended to use a list (1) because of reallocation
    and (2) because of index handling (the primes starts at 2, the
    list, 0)
    """
    primes = {n:None for n in range(2, n + 1)}

    for prime in list(primes.keys()):
        for number in list(primes.keys()):
            if prime != number and number%prime == 0:
                del primes[number]

    return primes


def switch(d: dict) -> dict:
    """
    1.7
    Switch keys and values of a dictionary given in argument
    """
    rst = dict()

    for k, v in d.items():
        rst[str(v)] = k

    return rst

def same_elements(l1: list, l2: list) -> bool:
    """
    1.8
    Check if two lists have the same elements, regardless of the number
    of elements
    """
    return is_anagram(uniq(l1), uniq(l2))

def is_anagram(l1: list, l2: list) -> bool:
    """
    1.8
    Check if two lists are anagrams: same elements but in order or in
    disorder
    """
    return (sorted(l1) == (sorted(l2)))

