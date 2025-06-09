from MonsterUtils import *
from WeaponConstants import *
from random import randint
from math import ceil


class Monster:
    def __init__(self, hp, defense, slashDefense, crushDefense, standardRangeDefense, heavyRangeDefense):
        self.hp = hp
        self.defense = defense
        self.slashDefense = slashDefense
        self.crushDefense = crushDefense
        self.standardRangeDefense = standardRangeDefense
        self.heavyRangeDefense = heavyRangeDefense
        self._isDead = False

    def setHp(self, dmg):
        self.hp -= dmg
        if self.hp <= 0:
            self._isDead = True

    def setExactHp(self, hp):
        self.hp = hp
        if self.hp <= 0:
            self._isDead = True

    def getHp(self):
        return self.hp

    def getDefense(self):
        return self.defense

    def setDefense(self, d):
        self.defense = d

    def isDead(self):
        return self._isDead

    def getSangVoid(self):
        dmg = getHit(sangMaxVoid, sangAttackRollVoid, self.defense, 0)
        self.setHp(dmg)

    def getSangVirtus(self):
        dmg = getHit(sangMaxVirtus, sangAttackRollVirtus, self.defense, 0)
        self.setHp(dmg)

    def getSangTorva(self):
        dmg = getHit(sangMaxTorva, sangAttackRollTorva, self.defense, 0)
        self.setHp(dmg)

    def getTbowVoid(self):
        dmg = getHit(tbowMaxVoid, tbowAttackRollVoid, self.defense, self.standardRangeDefense)
        self.setHp(dmg)

    def getTbowMasori(self):
        dmg = getHit(tbowMaxMasori, tbowAttackRollMasori, self.defense, self.standardRangeDefense)
        self.setHp(dmg)

    def getTbowTorva(self):
        dmg = getHit(tbowMaxTorva, tbowAttackRollTorva, self.defense, self.standardRangeDefense)
        self.setHp(dmg)

    def getChally(self):
        dmg = getChallyDamage(challyMaxHit, challyAttackRoll, self.defense, self.slashDefense)
        self.setHp(dmg)

    def getChallySalve(self):
        dmg = getHit(challySalveMaxHit, challyAttackRoll, self.defense, self.slashDefense)
        self.setHp(dmg)

    def getBgs(self):
        dmg = getHit(bgsMaxHit, bgsAttackRoll, self.defense, self.slashDefense)
        defense = max(self.defense - dmg, 0)
        self.setDefense(defense)
        self.setHp(dmg)

    def getBgsSalve(self):
        dmg = getHit(bgsMaxHitSalve, bgsSalveAttackRoll, self.defense, self.slashDefense)
        defense = max(self.defense - dmg, 0)
        self.setDefense(defense)
        self.setHp(dmg)

    def getMaulHit(self):
        dmg = getHit(maulMax, maulSpecAttackRoll, self.defense, self.crushDefense)
        defense = ceil(self.defense * 0.65)
        self.setDefense(defense)
        self.setHp(dmg)

    def getHornedMaulHit(self):
        dmg = getHornedDamage(maulMax)
        defense = ceil(self.defense * 0.65)
        self.setDefense(defense)
        self.setHp(dmg)

    def getScytheUltor(self):
        dmg = getScytheDamage(scytheOathMax, scytheOathAttackRoll, self.defense, self.slashDefense)
        self.setHp(dmg)

    def getScytheLb(self):
        dmg = getScytheDamage(scytheOathMaxLb, scytheOathAttackRoll, self.defense, self.slashDefense)
        self.setHp(dmg)

    def getScytheSalve(self):
        dmg = getScytheDamage(scytheMaxSalve, scytheSalveAttackRoll, self.defense, self.slashDefense)
        self.setHp(dmg)

    def getScythePneck(self):
        dmg = getScytheDamage(scytheMaxPneck, scythePneckAttackRoll, self.defense, self.slashDefense)
        self.setHp(dmg)

    def getClawSalve(self):
        dmg = getClawDamage(clawSpecMaxSalve, clawSalveAttackRoll, self.defense, self.slashDefense, False)
        self.setHp(dmg)

    def getZcb(self):
        dmg = getZcbDamage(zcbAttackRoll, self.defense, self.heavyRangeDefense)
        self.setHp(dmg)

    def getZcbSalve(self):
        dmg = getZcbDamage(zcbAttackRollSalve, self.defense, self.heavyRangeDefense)
        self.setHp(dmg)

    def getClaw(self):
        dmg = getClawDamage(clawSpecMax, clawAttackRoll, self.defense, self.slashDefense, False)
        self.setHp(dmg)
        return dmg

    def getHorendClaw(self):
        dmg = getClawDamage(clawSpecMax, clawAttackRoll, self.defense, self.slashDefense, True)
        self.setHp(dmg)
        return dmg

    def getThrallDamage(self):
        dmg = randint(0, 3)
        self.setHp(dmg)

    def getVengDamage(self, maxHit):
        dmg = 0.75 * randrange(maxHit)
        self.setHp(dmg)

    def doScytheAttack(self, maxHit, attackRoll):
        dmg = getScytheDamage(maxHit, attackRoll, self.defense, self.slashDefense)
        self.setHp(dmg)

    def doAttack(self, maxHit, attackRoll, typeDefense):
        dmg = getHit(maxHit, attackRoll, self.defense, typeDefense)
        self.setHp(dmg)
