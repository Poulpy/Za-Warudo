from random import randint

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

def addition_table(n: int) -> list:
    """
    1.5
    Returns the addition table given a integer
    """
    rst = [[i for i in range(n)] for j in range(n)]

    for i in range(1, n + 1):
        for j in range(1, n + 1):
            rst[i - 1][j - 1] = i + j

    return rst

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

def mystery_number(n: int):
    """
    2
    Game where the user must guess the number generated [0, 100] by the
    computer. The user can try n times, n given in argument
    """
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
    """
    3
    Game where each player roll the dice
    Game stops when a player reached n points
    A player rolls a dice till he got 1
    An even number increases the player's score
    3, the score is multiplied by 2
    5, the player loses 2 points
    """
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
