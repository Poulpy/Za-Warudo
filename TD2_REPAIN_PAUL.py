"""
Remove the duplicates in an unsorted list
"""
def uniq(l: list):
    i = 0
    while i != len(l):
        if l.count(l[i]) > 1:
            l.remove(l[i])
        else:
            i += 1

"""
Return a list removed form its duplicates
"""
def distinct(l: list) -> list:
    result = []
    i = 0

    while i != len(l):
        if result.count(l[i]) == 0:
            result.append(l[i])
        i += 1

    return result

"""
Remove the duplicates in an sorted list
"""
def sort_uniq(l: list):
    i = 0
    while i != len(l) - 1:
        if l[i] == l[i + 1]:
            l.remove(l[i])
        else:
            i += 1

"""
Flatten a multi dimensional list
[[1, 2], [2, 4]], gives : [1, 2, 2, 4]
"""
def flatten(l: list) -> list:
    flat_list = []

    for el in l:
        if isinstance(el, list):
            flat_list.extend(flatten(el))
        else:
            flat_list.append(el)

    return flat_list

"""
Return a list containing the successive integers in the list given in argument
"""
def successive_ints(l: list) -> list:
    rst = []

    for i in range(len(l) - 1):
        if l[i] == l[i + 1] - 1:
            rst.append([l[i], l[i + 1]])

    return rst

"""
Return a dictionnary, containing the number of occurrences of an int in the
list given in argument
"""
def occurrences(l: list) -> dict:
    d = dict()
    numbers = distinct(l)

    for el in l:
        d[el] = l.count(el)

    return d

"""
Returns the addition table given a integer
"""
def addition_table(n: int) -> list:
    rst = [[i for i in range(n)] for j in range(n)]

    for i in range(1, n + 1):
        for j in range(1, n + 1):
            rst[i - 1][j - 1] = i + j

    return rst

def switch(d: dict) -> dict:
    rst = dict()

    for k, v in d.items():
        rst[str(v)] = k

    return rst

def test_sort_uniq():
    l1 = [1, 2, 3, 3, 3, 4, 4, 6]
    print(l1)
    sort_uniq(l1)
    print(l1)

def test_uniq():
    l1 = [1, 2, 3, 2, 4, 1, 4, 3]
    print(l1)
    uniq(l1)
    print(l1)

def test_flatten():
    l1 = [[1, 2], [2, 4]]# gives : [1, 2, 2, 4]
    print(l1)
    print(flatten(l1))
    l2 = [[1, [34, [3, 90, 4]]], [2, 4]]# gives : [1, 2, 2, 4]
    print(l2)
    print(flatten(l2))

def test_successive_ints():
    l1 = [1, 2, 3, 4]
    print(successive_ints(l1))

def test_occurrences():
    l1 = [11, 33, 11, 33, 3, 0, 5]
    d1 = occurrences(l1)
    print(d1)

def test_addition():
    l1 = addition_table(6)
    print(l1)

def test_switch():
    l1 = [11, 33, 11, 33, 3, 0, 5]
    d1 = {"Marie":"3", "Bidule":"4"}
    print(d1)
    d2 = switch(d1)
    print(d2)


def main():
    test_sort_uniq()
    test_uniq()
    test_flatten()
    test_successive_ints()
    test_occurrences()
    test_addition()
    test_switch()


main()

