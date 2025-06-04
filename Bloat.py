from math import floor
from Monster import Monster
from random import randrange

MIN_DOWN_TICKS = 39
MAX_DOWN_TICKS = 53


class Bloat(Monster):
    def __init__(self, hp, defense, slashDefense, crushDefense, standardRangeDefense, heavyRangeDefense):
        Monster.__init__(self, hp, defense, slashDefense, crushDefense, standardRangeDefense, heavyRangeDefense)
        self.isWalking = True
        self.walkTime = randrange(MIN_DOWN_TICKS, MAX_DOWN_TICKS)

    def setHp(self, dmg):
        if self.isWalking:
            dmg = floor(dmg / 2)
        Monster.setHp(self, dmg)
        if self.hp <= 0:
            self._isDead = True

    def stopWalking(self):
        self.isWalking = False

    def getWalkTIme(self):
        return self.walkTime
