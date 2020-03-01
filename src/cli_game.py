from random import randint

def mystery_number(n: int):
    """
    2
    Game where the user must guess the number generated [0, 100] by the
    computer. The user can try n times, n given in argument
    """
    if n <= 0: raise ValueError("The number of trials can't be <= 0")

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
    if n <= 0: raise ValueError("The score can't be <= 0")

    player_points = [0, 0]
    current = 0

    while player_points[0] < n and player_points[1] < n:
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
            if player_points[current] > n:
                turn_end = True

        current = (current + 1) % 2

    print("Player %d won !" % (current))
    print("Scores : " + str(player_points))

