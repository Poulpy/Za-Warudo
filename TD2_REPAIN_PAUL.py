from random import randint

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

"""
Switch keys and values of a dictionary given in argument
"""
def switch(d: dict) -> dict:
    rst = dict()

    for k, v in d.items():
        rst[str(v)] = k

    return rst

"""
Check if two lists have the same elements, regardless of the number
of elements
"""
def same_elements(l1: list, l2: list) -> bool:
    return is_anagram(distinct(l1), distinct(l2))

"""
Check if two lists are anagrams: same elements but in order or in
disorder
"""
def is_anagram(l1: list, l2: list) -> bool:
    return (sorted(l1) == (sorted(l2)))

"""
Game where the user must guess the number generated [0, 100] by the
computer. The user can try n times, n given in argument
"""
def mystery_number(n: int):
    if n <= 0: return

    number_to_guess = randint(0, 100)
    i = 0
    won = False

    while i != n and not won:
        guess = int(input("Enter a number : "))

        if guess < number_to_guess:
            print("It is superior")
        elif guess > number_to_guess:
            print("It is inferior")
        else:
            print("You guessed right!")
            won = True

        i += 1

def dice_game(n: int):
    if n <= 0: return

    player_points = [0, 0]
    current = 0

    while player_points[0] < 50 and player_points[1] < 50:
        turn_end = False
        print("Turn of Player %d (%d)" % (current, player_points[current]))

        while not turn_end:
            print("Press enter to roll the dice")
            input()
            print("Rolling the dice...")
            dice = randint(1, 6)
            print("> %d" % (dice))

            if dice == 1:
                print("End of turn")
                turn_end = True
            elif dice%2 == 0:
                print("%d + %d" % (player_points[current], dice))
                player_points[current] += dice
            elif dice == 3:
                print("%d * 2" % (player_points[current]))
                player_points[current] *= 2
            elif dice == 5:
                print("%d - 2" % (player_points[current]))
                player_points[current] -= 2

            print("Total points at end of turn : %d" % (player_points[current]))
            if player_points[current] > 50:
                turn_end = True

        current = (current + 1) % 2

    print("Player %d won !" % (current))
    print("Scores : " + str(player_points))


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

def test_same_elements():
    l1 = [1, 1, 2, 4, 5, 4, 3]
    l2 = [5, 1, 2, 3, 4, 1, 1, 2]
    print(same_elements(l1, l2))# True
    l3 = [1, 1, 2, 4, 5, 4, 6]
    l4 = [5, 1, 2, 3, 4, 1, 1, 2]
    print(same_elements(l3, l4))# False

def test_is_anagram():
    l1 = "azerty"
    l2 = "ytreza"
    print(is_anagram(l1, l2))# True
    l1 = "azerty"
    l2 = "ytrezay"
    print(is_anagram(l1, l2))# False

def test_mystery_number():
    mystery_number(10)

def test_dice_game():
    dice_game(50)

def main():
    test_sort_uniq()
    test_uniq()
    test_flatten()
    test_successive_ints()
    test_occurrences()
    test_addition()
    test_switch()
    test_same_elements()
    test_is_anagram()
    #test_mystery_number()
    test_dice_game()


main()

