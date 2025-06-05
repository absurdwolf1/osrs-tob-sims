from Monster import Monster
from random import randrange


class Nylo(Monster):
    def __init__(self, hp, defense, slashDefense, crushDefense, standardRangeDefense, heavyRangeDefense):
        Monster.__init__(self, hp, defense, slashDefense, crushDefense, standardRangeDefense, heavyRangeDefense)
        self.godBoss = False
        self.phase = "melee"
        self.phases = ["melee", "range", "mage"]
        # keeps track of how many of each phase the boss turns to [melee, range, mage]
        # it starts in melee phase
        self.phaseTypeCounts = [1, 0, 0]

    def forceGodBoss(self):
        self.godBoss = True

    def changePhase(self):
        if self.godBoss:
            if self.phase == "melee":
                self.setPhase("range")
                return
            else:
                self.setPhase("melee")
                return

        roll = randrange(2)

        if self.phase == "melee":
            self.setPhase("range") if roll == 0 else self.setPhase("mage")
        elif self.phase == "range":
            self.setPhase("melee") if roll == 0 else self.setPhase("mage")
        elif self.phase == "mage":
            self.setPhase("melee") if roll == 0 else self.setPhase("range")

    def setPhase(self, newPhase):
        if newPhase == "melee":
            self.phaseTypeCounts[0] += 1
            self.phase = "melee"
        elif newPhase == "range":
            self.phaseTypeCounts[1] += 1
            self.phase = "range"
        elif newPhase == "mage":
            self.phaseTypeCounts[2] += 1
            self.phase = "mage"
