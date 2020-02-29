# Repain Paul
# IATIC 3

from math import sqrt

# Exercice 1
def exercice1():
    # 1
    temps = 6.892
    distance = 19.7
    vitesse = distance / temps
    # C-like formatting
    # the number after the dot . gives the precision
    print(format(vitesse, '.1f'))
    print("%.1f" % vitesse)

    # 2
    nom = input("Entrez votre nom : ")
    age = input("Entrez age : ")
    print("Nom : " + nom + ", age : " + age)

# Exercice 2
def exercice2():
    # 1
    f = float(input("Entrez un flottant : "))
    if f < 0:
        raise ValueError("Can't be < 0")
    else:
        print("Racine carré : " + str(sqrt(f)))

    # 2
    s1 = input("Entrez une string : ")
    s2 = input("Entrez une string : ")

    # 3
    if s1 < s2:
        print("{} plus petit que {}".format(s1, s2))
    else:
        print("%s plus petit que %s" % (s2, s1))

    p_seuil = 2.3
    v_seuil = 7.41

    pression = int(input("Entrez la pression : "))
    volume = int(input("Entrez le volume courant de l'enceinte : "))

    if pression > p_seuil and volume > v_seuil:
        print("Arret")
    elif pression > p_seuil:
        print("Augmentez le volume")
    elif volume > v_seuil:
        print("Diminuez le volume")
    else:
        print("Tout va bien")

    # 3
    a = 0
    b = 10

    print("On affiche 0 -> 9")
    while a < b:
        print(a)
        a += 1

    # 4
    print("On affiche b s'il est impair")
    while b != 0:
        if b % 2 != 0:
            print(str(b))
        b -= 1

    # 5
    chaine = "chaine"
    print("On affiche chaque caractère de la chaine %s" % (chaine))
    for char in chaine:
        print(char)

    # 6
    print("On affiche les nombres de 0 à 15 exclu, avec un pas de 3")
    for i in range(0, 15, 3):
        print(str(i))

def exercice3():
    letter = input("Saisissez une lettre (B/b/V/v/R/r) : ")
    if letter == "B" or letter == "b":
        print("Bleu")
    elif letter == "V" or letter == "v":
        print("Vert")
    elif letter == "R" or letter == "r":
        print("Rouge")
    else:
        print("Couleur non reconnue")

def exercice4():
    number = int(input("Entrez un entier naturel : "))
    # 1
    size = count_digits(number)
    print("Nombre de digits : " + str(size))
    # 2
    # for d in str(number)[::-1]:
    # reversed() : retourne une chaine a l'envers
    for d in reversed(str(number)):
        print(d)

"""
Returns the number of digits of a NATURAL number
Converts to a string, then counts the number of characters in the string
"""
def count_digits(natural: int) -> int:
    return len(str(natural))

def main():
    exercice1()
    exercice2()
    exercice3()
    exercice4()

main()

