from math import floor
from random import randrange
from random import randint


def getHit(maxHit, attRoll, defense, slashDefense):
    accuracy = getAccuracy(attRoll, getDefRoll(defense, slashDefense))
    return getDamage(maxHit, accuracy)


def getHornedDamage(maxHit):
    # randrange return a random int between [start, stop)
    # since stop is non-inclusive, add 1 to the max hit
    dmg = randrange(0, maxHit + 1, 1)
    # if the damage rolled is a 0, transform it into a 1
    if dmg == 0:
        return 1
    return dmg


def getDefRoll(defense, targetStyleDefBonus):
    return (defense + 9) * (64 + targetStyleDefBonus)


def getAccuracy(attRoll, defRoll):
    if attRoll > defRoll:
        hitChance = 1 - ((defRoll + 2) / (2 * (attRoll + 1)))
    else:
        hitChance = attRoll / (2 * (defRoll + 1))
    return round(hitChance * 100, 2)


def getScytheDamage(scytheMax, attRoll, defense, slashDefense):
    damage = 0
    accuracy = getAccuracy(attRoll, getDefRoll(defense, slashDefense))
    for x in [1, 2, 4]:
        scytheMaxHitSplat = floor(scytheMax / x)
        damage += getDamage(scytheMaxHitSplat, accuracy)
    return damage


def accuracyCheck(hitChance):
    # hit chance is a percent rounded to 2 decimals, multiply by 100 so we can roll a random int against it
    hitChance *= 100
    return hitChance >= randint(0, 1000)


def getDamage(maxHit, accuracy):
    # pass accuracy check
    if accuracyCheck(accuracy):
        dmg = randint(0, maxHit)
        # if the damage rolled is a 0, transform it into a 1
        if dmg == 0:
            return 1
        return dmg
    else:
        return 0


def getChallyDamage(maxHit, attRoll, defense, slashDefense):
    accuracy = getAccuracy(attRoll, getDefRoll(defense, slashDefense))
    secondHitAccuracy = max(0, accuracy - 25)
    dmg = getDamage(maxHit, accuracy)
    dmg += getDamage(maxHit, secondHitAccuracy)
    return dmg


def getZcbDamage(attRoll, defense, heavyRangedDefense):
    accuracy = getAccuracy(attRoll, getDefRoll(defense, heavyRangedDefense))
    return 110 if accuracyCheck(accuracy) else 0


def getClawDamage(maxHit, attRoll, d, slashDefense, horned):
    accuracy = getAccuracy(attRoll, getDefRoll(d, slashDefense))
    # first hitsplat
    # accuracy check
    if accuracyCheck(accuracy):
        firstHit = randrange(floor(maxHit / 2), maxHit)
        secondHit = floor(firstHit / 2)
        thirdHit = floor(secondHit / 2)
        forthHit = thirdHit + 1

    # second hitsplat
    elif accuracyCheck(accuracy) or horned:
        firstHit = 0
        secondHit = randrange(floor(maxHit * 3/8), floor(maxHit * 7/8))
        thirdHit = floor(secondHit / 2)
        forthHit = thirdHit + 1

    # third hitsplat
    elif accuracyCheck(accuracy):
        firstHit = 0
        secondHit = 0
        thirdHit = randrange(floor(maxHit * 1/4), floor(maxHit * 3/4))
        forthHit = thirdHit + 1

    # forth hitsplat
    elif accuracyCheck(accuracy):
        firstHit = 0
        secondHit = 0
        thirdHit = 0
        forthHit = randrange(floor(maxHit * 1/4), floor(maxHit * 5/4))
    else:
        # 2/3 chance of rolling 2 damage when you miss all the other accuracy checks
        if accuracyCheck(66.67):
            firstHit = 1
            secondHit = 1
        else:
            firstHit = 0
            secondHit = 0
        thirdHit = 0
        forthHit = 0
    return firstHit + secondHit + thirdHit + forthHit
