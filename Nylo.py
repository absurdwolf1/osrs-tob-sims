from Monster import Monster
from random import randrange


class Nylo(Monster):
    def __init__(self, hp, defense, slashDefense, crushDefense, standardRangeDefense, heavyRangeDefense):
        Monster.__init__(self, hp, defense, slashDefense, crushDefense, standardRangeDefense, heavyRangeDefense)
        self.godBoss = False
        self.phase = "melee"
        self.phases = ["melee", "range", "mage"]

    def forceGodBoss(self):
        self.godBoss = True

    def changePhase(self):
        if self.godBoss:
            if self.phase == "melee":
                return "range"
            else:
                return "melee"

        roll = randrange(2)

        if self.phase == "melee":
            self.phase = "range" if roll == 0 else self.phase = "mage"
        elif self.phase == "range":
            self.phase = "melee" if roll == 0 else self.phase = "mage"
        elif self.phase == "mage":
            self.phase = "melee" if roll == 0 else self.phase = "range"
        return self.phase
