from math import floor
from random import randrange


def getHit(maxHit, attRoll, defense, slashDefense):
    accuracy = getHitChance(attRoll, getDefRoll(defense, slashDefense))
    return getHitSplat(maxHit, accuracy)


def getHornedHit(maxHit):
    return randrange(maxHit)


def getDefRoll(defense, targetStyleDefBonus):
    return (defense + 9) * (64 + targetStyleDefBonus)


def getHitChance(attRoll, defRoll):
    if attRoll > defRoll:
        hitChance = 1 - ((defRoll + 2) / (2 * (attRoll + 1)))
    else:
        hitChance = attRoll / (2 * (defRoll + 1))
    return floor(hitChance * 100)


def getScytheHit(scytheMax, attRoll, defense, slashDefense):
    damage = 0
    accuracy = getHitChance(attRoll, getDefRoll(defense, slashDefense))
    for x in [1, 2, 4]:
        scytheMaxHitSplat = floor(scytheMax / x)
        damage += getHitSplat(scytheMaxHitSplat, accuracy)
    return damage


def getHitSplat(maxHit, accuracy):
    # pass accuracy check
    if accuracy >= randrange(100):
        # get damage
        return randrange(maxHit)
    else:
        return 0


def getZcbDamage(attRoll, defense, slashDefense):
    accuracy = getHitChance(attRoll, getDefRoll(defense, slashDefense))
    return 110 if accuracy >= randrange(100) else 0


def getHornedClaw(maxHit):
    firstHit = randrange(floor(maxHit / 2), maxHit)
    secondHit = floor(firstHit / 2)
    thirdHit = floor(secondHit / 2)
    forthHit = thirdHit + 1
    return firstHit + secondHit + thirdHit + forthHit


def getClawDamage(maxHit, attRoll, d, slashDefense):
    accuracy = getHitChance(attRoll, getDefRoll(d, slashDefense))
    # first hitsplat
    # accuracy check
    if accuracy >= randrange(100):
        firstHit = randrange(floor(maxHit / 2), maxHit)
        secondHit = floor(firstHit / 2)
        thirdHit = floor(secondHit / 2)
        forthHit = thirdHit + 1

    # second hitsplat
    elif accuracy >= randrange(100):
        firstHit = 0
        secondHit = randrange(floor(maxHit * 3/8), floor(maxHit * 7/8))
        thirdHit = floor(secondHit / 2)
        forthHit = thirdHit + 1

    # third hitsplat
    elif accuracy >= randrange(100):
        firstHit = 0
        secondHit = 0
        thirdHit = randrange(floor(maxHit * 1/4), floor(maxHit * 3/4))
        forthHit = thirdHit + 1

    # forth hitsplat
    elif accuracy >= randrange(100):
        firstHit = 0
        secondHit = 0
        thirdHit = 0
        forthHit = randrange(floor(maxHit * 1/4), floor(maxHit * 5/4))
    else:
        if 66 > randrange(66):
            firstHit = 1
            secondHit = 1
        else:
            firstHit = 0
            secondHit = 0
        thirdHit = 0
        forthHit = 0
    return firstHit + secondHit + thirdHit + forthHit


def calculateVengDamage(numberOfVengsPerPerson, teamSize, maxHit):
    numberOfVengs = teamSize * numberOfVengsPerPerson
    dmg = 0
    for x in range(numberOfVengs):
        dmg += 0.75 * randrange(maxHit)

    return dmg
